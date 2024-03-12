from .usage import *


def create_savings_plans_custom_line_items(inclusive_start_billing_period, exclusive_end_billing_period,
                                           is_dry_run=True, include_fargate_for_savings_plans=False,
                                           include_lambda_for_savings_plans=False):
    start_date_string = inclusive_start_billing_period.strftime('%Y-%m-%d')
    end_date_string = exclusive_end_billing_period.strftime('%Y-%m-%d')
    inclusive_start_billing_period_string = inclusive_start_billing_period.strftime(
        '%Y-%m')
    exclusive_end_billing_period_string = exclusive_end_billing_period.strftime(
        '%Y-%m')
    custom_line_items = []
    billing_conductor_client = boto3.client('billingconductor')
    cost_explorer_client = boto3.client('ce')
    # note that end date is exclusive
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_savings_plans_utilization_details.html
    time_period = {'Start': start_date_string, 'End': end_date_string}
    savings_plans_details = cost_explorer_client.get_savings_plans_utilization_details(TimePeriod=time_period).get(
        'SavingsPlansUtilizationDetails', [])
    # by default this uses the current billing period
    # since the line items are applied for the previous month, use the inclusive start billing period
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_account_associations.html
    account_associations = billing_conductor_client.list_account_associations(
        BillingPeriod=inclusive_start_billing_period_string)
    # eligible accounts are defined as belonging to a billing group
    eligible_linked_accounts = [account for account in account_associations.get('LinkedAccounts', []) if
                                account.get('BillingGroupArn')]
    normalized_hours_by_account = {}
    total_eligible_compute_running_hours = Decimal(0.0)
    compute_description_text = 'EC2, '
    ec2_normalized_instance_hours_by_linked_account = get_ec2_normalized_hours_by_linked_account(
        start_date_string, end_date_string)
    if include_fargate_for_savings_plans:
        fargate_vcpu_hours_by_linked_account = get_fargate_vcpu_hours_by_linked_account(
            start_date_string, end_date_string)
        compute_description_text += 'Fargate, '
    if include_lambda_for_savings_plans:
        lambda_gb_hours_by_linked_account = get_lambda_gb_hours_by_linked_account(
            start_date_string, end_date_string)
        compute_description_text += 'Lambda, '
    # only include running hours from accounts that belong to billing groups
    for account in eligible_linked_accounts:
        account_id = account.get('AccountId')
        ec2_normalized_hours_for_account = ec2_normalized_instance_hours_by_linked_account.get(
            account_id, Decimal(0.0))
        total_eligible_compute_running_hours += ec2_normalized_hours_for_account
        normalized_hours_by_account[account_id] = ec2_normalized_hours_for_account
        if include_fargate_for_savings_plans:
            total_eligible_compute_running_hours += fargate_vcpu_hours_by_linked_account.get(
                account_id, Decimal(0.0))
            normalized_hours_by_account[account_id] += fargate_vcpu_hours_by_linked_account.get(account_id,
                                                                                                Decimal(0.0))
        if include_lambda_for_savings_plans:
            total_eligible_compute_running_hours += lambda_gb_hours_by_linked_account.get(
                account_id, Decimal(0.0))
            normalized_hours_by_account[account_id] += lambda_gb_hours_by_linked_account.get(
                account_id, Decimal(0.0))
    for savings_plan in savings_plans_details:
        for account in eligible_linked_accounts:
            savings_plan_guid = savings_plan.get(
                'SavingsPlanArn').split('/')[-1]
            savings_plan_account_id = savings_plan.get(
                'Attributes').get('AccountId')
            # ignore Savings Plans purchases made in accounts that belong to a billing group since ABC processes them
            # https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html#bp-dataset
            if savings_plan_account_id not in [billing_group_account['AccountId'] for billing_group_account in
                                               eligible_linked_accounts]:
                running_hour_percentage = Decimal(
                    normalized_hours_by_account.get(account.get('AccountId', Decimal(0.0)),
                                                    Decimal(0.0))) / total_eligible_compute_running_hours
                account_benefit = Decimal(savings_plan.get('Savings').get(
                    'NetSavings')) * running_hour_percentage
                charge_type = 'Credit' if account_benefit >= 0 else 'Fee'
                new_custom_line_item = {
                    'Name': f'SavingsPlan-{savings_plan_guid}-Account-{account.get("AccountId")}-Benefit-{start_date_string}',
                    'Description': f'{charge_type} from {savings_plan.get("SavingsPlanArn")} for {account.get("AccountName")} based on {round(running_hour_percentage * 100, 2)}% of normalized hours for {compute_description_text.rstrip(', ')}',
                    'BillingGroupArn': account.get('BillingGroupArn'),
                    'BillingPeriodRange': {'InclusiveStartBillingPeriod': inclusive_start_billing_period_string,
                                           'ExclusiveEndBillingPeriod': exclusive_end_billing_period_string},
                    'ChargeDetails': {
                        # if the commitment has negative savings, distribute the charges as a fee
                        'Flat': {'ChargeValue': float(abs(account_benefit))},
                        'Type': charge_type.upper()
                    },
                    'AccountId': account.get('AccountId')
                }
                # ignore accounts without matching usage
                if account_benefit != 0:
                    custom_line_items.append(new_custom_line_item)
                    if not is_dry_run:
                        billing_conductor_client.create_custom_line_item(
                            **new_custom_line_item)
    return custom_line_items
