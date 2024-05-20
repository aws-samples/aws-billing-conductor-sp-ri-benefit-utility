from datetime import *
from sam_sp_ri_utility.services.savings_plans import *
from unittest import mock
from .utilities import *

default_account_associations_response = {
    'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                         'HTTPHeaders': {'content-type': 'application/json', 'content-length': '818',
                                         'connection': 'keep-alive', 'date': 'Thu, 07 Mar 2024 22:47:50 GMT',
                                         'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                         'x-amzn-remapped-x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                         'x-amzn-remapped-content-length': '818',
                                         'x-amz-apigw-id': 'UR-TlFlJoAMEc6g=',
                                         'x-amzn-trace-id': '8a94e821-2206-439b-9267-3856ff64203e',
                                         'x-amzn-remapped-date': 'Thu, 07 Mar 2024 22:47:50 GMT',
                                         'x-cache': 'Miss from cloudfront',
                                         'via': '1.1 d819e0fec943c45d31b55f5dce0b44ee.cloudfront.net (CloudFront)',
                                         'x-amz-cf-pop': 'LAX50-P1',
                                         'x-amz-cf-id': '17QFv1qUHyntsVT8tgLVIWEwyxKq8oquZf0pICNDw4ghhZGqHdI-Xw=='},
                         'RetryAttempts': 0}, 'LinkedAccounts': [
        {'AccountId': '111111111111', 'AccountName': 'Audit',
            'AccountEmail': 'ct-audit@example.com'},
        {'AccountId': '222222222222', 'AccountName': 'Log Archive',
         'AccountEmail': 'ct-logarchive@example.com'},
        {'AccountId': '789456123012', 'AccountName': 'payer',
         'AccountEmail': 'payer@example.com'},
        {'AccountId': '444444444444',
         'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
         'AccountName': 'Secondary Sandbox', 'AccountEmail': 'ct-secondary-sandbox@example.com'},
        {'AccountId': '555555555555',
         'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
         'AccountName': 'General Sandbox', 'AccountEmail': 'ct-general-sandbox@example.com'}]}


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_standard_input(mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for Secondary Sandbox based on 38.89% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.2391880032}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for General Sandbox based on 61.11% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.9472954336}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'},
                {'Name': 'SavingsPlan-8879e313-a9fa-4f68-b364-1d582619fba2-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2 for Secondary Sandbox based on 38.89% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.0465777868}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-8879e313-a9fa-4f68-b364-1d582619fba2-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2 for General Sandbox based on 61.11% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.6446222364}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'},
                {'Name': 'SavingsPlan-e58e258d-e374-4468-becf-69ceee7fd3fc-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/e58e258d-e374-4468-becf-69ceee7fd3fc for Secondary Sandbox based on 38.89% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.3174041197333335}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-e58e258d-e374-4468-becf-69ceee7fd3fc-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/e58e258d-e374-4468-becf-69ceee7fd3fc for General Sandbox based on 61.11% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.070206473866667}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'},
                {'Name': 'SavingsPlan-67e19d7f-3dd7-4652-861b-a7fb6dd11892-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892 for Secondary Sandbox based on 38.89% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.1919272702666667}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-67e19d7f-3dd7-4652-861b-a7fb6dd11892-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892 for General Sandbox based on 61.11% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.3015999961333334}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'Partial Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.00497717',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '44.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                 'AmortizedUpfrontCommitment': '3.49588968', 'TotalAmortizedCommitment': '6.96'}},
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'No Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.01',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '0.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '2.6912000232', 'OnDemandCostEquivalent': '9.6512000232'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '6.96', 'AmortizedUpfrontCommitment': '0.0',
                                 'TotalAmortizedCommitment': '6.96'}},
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/e58e258d-e374-4468-becf-69ceee7fd3fc',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:57.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'All Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.0',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/e58e258d-e374-4468-becf-69ceee7fd3fc',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:58.000Z',
                                            'Status': 'Active', 'UpfrontFee': '87.6'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '3.3876105936000003', 'OnDemandCostEquivalent': '10.3476105936'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '0.0', 'AmortizedUpfrontCommitment': '6.96',
                                 'TotalAmortizedCommitment': '6.96'}},
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2025-01-30T01:09:15.000Z', 'HourlyCommitment': '0.001', 'InstanceFamily': 't3a',
                        'PaymentOption': 'All Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.0',
                        'Region': 'US West (Oregon)',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892',
                        'SavingsPlansType': 'EC2InstanceSavingsPlans', 'StartDateTime': '2024-01-31T01:09:16.000Z',
                                            'Status': 'Active', 'UpfrontFee': '8.76'},
         'Utilization': {'TotalCommitment': '0.6960000000000001', 'UsedCommitment': '0.6960000000000001',
                         'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '0.49352726640000005', 'OnDemandCostEquivalent': '1.1895272664'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '0.0',
                                 'AmortizedUpfrontCommitment': '0.6960000000000001',
                                 'TotalAmortizedCommitment': '0.6960000000000001'}}], 'Total': {
        'Utilization': {'TotalCommitment': '21.5760000000000001', 'UsedCommitment': '21.5760000000000001',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '9.75882132000000035', 'OnDemandCostEquivalent': '31.3348213200'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '10.42411032',
                                'AmortizedUpfrontCommitment': '11.1518896800000001',
                                'TotalAmortizedCommitment': '21.5760000000000001'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {'555555555555': Decimal(
        '7656'), '444444444444': Decimal('4872')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, False, False)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_commitment_purchased_in_billing_group(mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for Secondary Sandbox based on 50.00% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.5932417184}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for General Sandbox based on 50.00% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.5932417184}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'Partial Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.00497717',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '44.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                 'AmortizedUpfrontCommitment': '3.49588968', 'TotalAmortizedCommitment': '6.96'}},
        {'SavingsPlanArn': 'arn:aws:savingsplans::555555555555:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2',
         'Attributes': {'AccountId': '555555555555', 'AccountName': 'General Sandbox',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'No Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.01',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::555555555555:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '0.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '5.87768346', 'OnDemandCostEquivalent': '9.6512000232'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '10.42411032', 'AmortizedUpfrontCommitment': '0.0',
                                 'TotalAmortizedCommitment': '6.96'}},
    ], 'Total': {
        'Utilization': {'TotalCommitment': '13.92', 'UsedCommitment': '13.92',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '9.75882132000000035', 'OnDemandCostEquivalent': '19.79768346'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '10.42411032',
                                'AmortizedUpfrontCommitment': '11.1518896800000001',
                                'TotalAmortizedCommitment': '13.92'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {
        '555555555555': Decimal('50'), '444444444444': Decimal('50')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, False, False)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_negative_net_savings(mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Fee from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for Secondary Sandbox based on 50.00% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.5932417184}, 'Type': 'FEE'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Fee from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for General Sandbox based on 50.00% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.5932417184}, 'Type': 'FEE'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'Partial Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.00497717',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '44.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '0.0', 'UnusedCommitment': '6.96',
                         'UtilizationPercentage': '0'},
         'Savings': {'NetSavings': '-3.1864834368', 'OnDemandCostEquivalent': '0'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                 'AmortizedUpfrontCommitment': '3.49588968', 'TotalAmortizedCommitment': '6.96'}}
    ], 'Total': {
        'Utilization': {'TotalCommitment': '13.92', 'UsedCommitment': '13.92',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '9.75882132000000035', 'OnDemandCostEquivalent': '19.79768346'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                'AmortizedUpfrontCommitment': '3.49588968',
                                'TotalAmortizedCommitment': '6.96'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {
        '555555555555': Decimal('50'), '444444444444': Decimal('50')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, False, False)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_fargate_vcpu_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_fargate_usage(mock_fargate_usage, mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for Secondary Sandbox based on 33.33% of normalized hours for EC2, Fargate',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.0621611456}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for General Sandbox based on 66.67% of normalized hours for EC2, Fargate',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.1243222912}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'Partial Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.00497717',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '44.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                 'AmortizedUpfrontCommitment': '3.49588968', 'TotalAmortizedCommitment': '6.96'}},
        {'SavingsPlanArn': 'arn:aws:savingsplans::555555555555:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2',
         'Attributes': {'AccountId': '555555555555', 'AccountName': 'General Sandbox',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'No Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.01',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::555555555555:savingsplan/8879e313-a9fa-4f68-b364-1d582619fba2',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '0.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '5.87768346', 'OnDemandCostEquivalent': '9.6512000232'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '10.42411032', 'AmortizedUpfrontCommitment': '0.0',
                                 'TotalAmortizedCommitment': '6.96'}},
    ], 'Total': {
        'Utilization': {'TotalCommitment': '13.92', 'UsedCommitment': '13.92',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '9.75882132000000035', 'OnDemandCostEquivalent': '19.79768346'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '10.42411032',
                                'AmortizedUpfrontCommitment': '11.1518896800000001',
                                'TotalAmortizedCommitment': '13.92'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {'555555555555': Decimal(
        '100'), '444444444444': Decimal('50')}
    mock_fargate_usage.return_value = {
        '555555555555': Decimal('100'), '444444444444': Decimal('50')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, True, False)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_lambda_gb_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_lambda_usage(mock_lambda_usage, mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for Secondary Sandbox based on 33.33% of normalized hours for EC2, Lambda',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.0621611456}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for General Sandbox based on 66.67% of normalized hours for EC2, Lambda',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.1243222912}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'Partial Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.00497717',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '44.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                 'AmortizedUpfrontCommitment': '3.49588968', 'TotalAmortizedCommitment': '6.96'}}
    ], 'Total': {
        'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                'AmortizedUpfrontCommitment': '3.49588968',
                                'TotalAmortizedCommitment': '6.96'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {'555555555555': Decimal(
        '199'), '444444444444': Decimal('99')}
    mock_lambda_usage.return_value = {
        '555555555555': Decimal('1'), '444444444444': Decimal('1')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, False, True)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_fargate_vcpu_hours_by_linked_account')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_lambda_gb_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_fargate_and_lambda_usage(mock_lambda_usage, mock_fargate_usage,
                                                                             mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for Secondary Sandbox based on 33.33% of normalized hours for EC2, Fargate, Lambda',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.0621611456}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-53e79e9c-5a3b-40ea-8096-f6876496613a-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a for General Sandbox based on 66.67% of normalized hours for EC2, Fargate, Lambda',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.1243222912}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2024-12-05T18:24:56.000Z', 'HourlyCommitment': '0.01', 'InstanceFamily': '',
                        'PaymentOption': 'Partial Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.00497717',
                        'Region': 'Any',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a',
                        'SavingsPlansType': 'ComputeSavingsPlans', 'StartDateTime': '2023-12-06T18:24:57.000Z',
                                            'Status': 'Active', 'UpfrontFee': '44.0'},
         'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96', 'UnusedCommitment': '0.0',
                         'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                 'AmortizedUpfrontCommitment': '3.49588968', 'TotalAmortizedCommitment': '6.96'}}
    ], 'Total': {
        'Utilization': {'TotalCommitment': '6.96', 'UsedCommitment': '6.96',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '3.1864834368', 'OnDemandCostEquivalent': '10.1464834368'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '3.46411032',
                                'AmortizedUpfrontCommitment': '3.49588968',
                                'TotalAmortizedCommitment': '6.96'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {'555555555555': Decimal(
        '198'), '444444444444': Decimal('98')}
    mock_fargate_usage.return_value = {
        '555555555555': Decimal('1'), '444444444444': Decimal('1')}
    mock_lambda_usage.return_value = {
        '555555555555': Decimal('1'), '444444444444': Decimal('1')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, True, True)
    assert is_equal_list_of_dict(actual, expected)

@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.savings_plans.get_ec2_normalized_hours_by_linked_account')
def test_create_savings_plans_custom_line_items_for_standard_input_specify_arns(mock_ec2_usage, mock_client):
    expected = [{'Name': 'SavingsPlan-67e19d7f-3dd7-4652-861b-a7fb6dd11892-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892 for Secondary Sandbox based on 38.89% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.1919272702666667}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'SavingsPlan-67e19d7f-3dd7-4652-861b-a7fb6dd11892-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892 for General Sandbox based on 61.11% of normalized hours for EC2',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.3015999961333334}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_savings_plans_utilization_details.return_value = {'SavingsPlansUtilizationDetails': [
        {'SavingsPlanArn': 'arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892',
         'Attributes': {'AccountId': '789456123012', 'AccountName': 'payer',
                        'EndDateTime': '2025-01-30T01:09:15.000Z', 'HourlyCommitment': '0.001', 'InstanceFamily': 't3a',
                        'PaymentOption': 'All Upfront', 'PurchaseTerm': '1yr', 'RecurringHourlyFee': '0.0',
                        'Region': 'US West (Oregon)',
                        'SavingsPlanARN': 'arn:aws:savingsplans::789456123012:savingsplan/67e19d7f-3dd7-4652-861b-a7fb6dd11892',
                        'SavingsPlansType': 'EC2InstanceSavingsPlans', 'StartDateTime': '2024-01-31T01:09:16.000Z',
                                            'Status': 'Active', 'UpfrontFee': '8.76'},
         'Utilization': {'TotalCommitment': '0.6960000000000001', 'UsedCommitment': '0.6960000000000001',
                         'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
         'Savings': {'NetSavings': '0.49352726640000005', 'OnDemandCostEquivalent': '1.1895272664'},
         'AmortizedCommitment': {'AmortizedRecurringCommitment': '0.0',
                                 'AmortizedUpfrontCommitment': '0.6960000000000001',
                                 'TotalAmortizedCommitment': '0.6960000000000001'}}], 'Total': {
        'Utilization': {'TotalCommitment': '21.5760000000000001', 'UsedCommitment': '21.5760000000000001',
                        'UnusedCommitment': '0.0', 'UtilizationPercentage': '100'},
        'Savings': {'NetSavings': '9.75882132000000035', 'OnDemandCostEquivalent': '31.3348213200'},
        'AmortizedCommitment': {'AmortizedRecurringCommitment': '10.42411032',
                                'AmortizedUpfrontCommitment': '11.1518896800000001',
                                'TotalAmortizedCommitment': '21.5760000000000001'}},
        'TimePeriod': {'Start': '2024-02-01',
                       'End': '2024-03-01'},
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Thu, 07 Mar 2024 22:44:25 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4301',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'},
        'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_ec2_usage.return_value = {'555555555555': Decimal(
        '7656'), '444444444444': Decimal('4872')}
    actual = create_savings_plans_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, False, False, 'arn:aws:savingsplans::789456123012:savingsplan/53e79e9c-5a3b-40ea-8096-f6876496613a')
    assert is_equal_list_of_dict(actual, expected)