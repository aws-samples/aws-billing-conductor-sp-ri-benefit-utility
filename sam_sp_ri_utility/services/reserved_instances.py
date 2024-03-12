from .usage import *


def create_reserved_instances_custom_line_items(inclusive_start_billing_period, exclusive_end_billing_period,
                                                is_dry_run=True):
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
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_reservation_utilization.html
    time_period = {'Start': start_date_string, 'End': end_date_string}
    # supported values:
    # Amazon Elastic Compute Cloud - Compute
    # Amazon Relational Database Service
    # Amazon ElastiCache
    # Amazon Redshift
    # Amazon Elasticsearch Service
    # Amazon OpenSearch Service
    # Amazon MemoryDB
    filter = {'Dimensions': {'Key': 'SERVICE', 'Values': [
        'Amazon Relational Database Service']}}
    group_by = [{'Type': 'DIMENSION', 'Key': 'SUBSCRIPTION_ID'}]
    rds_reserved_instances_details = \
        cost_explorer_client.get_reservation_utilization(Filter=filter, TimePeriod=time_period, GroupBy=group_by).get(
            'UtilizationsByTime', [])[0].get('Groups', [])
    # by default this uses the current billing period
    # since the line items are applied for the previous month, use the inclusive start billing period
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/client/list_account_associations.html
    account_associations = billing_conductor_client.list_account_associations(
        BillingPeriod=inclusive_start_billing_period_string)
    # eligible accounts are defined as belonging to a billing group
    eligible_linked_accounts = [account for account in account_associations['LinkedAccounts'] if
                                account.get('BillingGroupArn')]
    normalized_instance_hours_by_account = get_rds_normalized_hours_by_linked_account(start_date_string,
                                                                                      end_date_string)
    total_eligible_rds_running_hours = Decimal(0.0)
    # only include running hours from accounts that belong to billing groups
    for account in eligible_linked_accounts:
        total_eligible_rds_running_hours += normalized_instance_hours_by_account.get(account.get('AccountId'),
                                                                                     Decimal(0.0))
    for reserved_instance in rds_reserved_instances_details:
        for account in eligible_linked_accounts:
            reserved_instance_account_id = reserved_instance.get(
                'Attributes').get('accountId')
            # ignore Reserved Instances purchases made in accounts that belong to a billing group since ABC handles them
            # https://docs.aws.amazon.com/billingconductor/latest/userguide/best-practices.html#bp-dataset
            if reserved_instance_account_id not in [billing_group_account['AccountId'] for billing_group_account in
                                                    eligible_linked_accounts]:
                reserved_instance_id = reserved_instance.get(
                    'Attributes').get('reservationARN').split(':')[-1]
                rds_running_hour_percentage = Decimal(
                    normalized_instance_hours_by_account.get(account.get('AccountId'),
                                                             Decimal(0.0))) / total_eligible_rds_running_hours
                account_benefit = Decimal(
                    reserved_instance.get('Utilization').get('NetRISavings')) * rds_running_hour_percentage
                charge_type = 'Credit' if account_benefit >= 0 else 'Fee'
                new_custom_line_item = {
                    'Name': f'ReservedInstance-{reserved_instance_id}-Account-{account.get("AccountId")}-Benefit-{start_date_string}',
                    'Description': f'{charge_type} from {reserved_instance.get("Attributes").get("reservationARN")} for {account.get("AccountId")} based on {round(rds_running_hour_percentage * 100, 2)}% of RDS normalized instance hours',
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
