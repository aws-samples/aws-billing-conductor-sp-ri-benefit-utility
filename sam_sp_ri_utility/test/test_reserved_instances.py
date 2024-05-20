from datetime import *
from sam_sp_ri_utility.services.reserved_instances import *
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
@mock.patch('sam_sp_ri_utility.services.reserved_instances.get_rds_normalized_hours_by_linked_account')
def test_create_reserved_instances_custom_line_items_for_standard_input(mock_rds_usage, mock_client):
    expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 74.80% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 3.0712797826345812}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 25.20% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 1.034802407365419}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-50-52-761-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-52-761 for 444444444444 based on 74.80% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.9338804243904972}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-50-52-761-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-52-761 for 555555555555 based on 25.20% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.9885086156095026}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-51-29-735-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-51-29-735 for 444444444444 based on 74.80% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.655040550086921}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-51-29-735-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-51-29-735 for 555555555555 based on 25.20% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.8945594499130791}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_reservation_utilization.return_value = {'UtilizationsByTime': [
        {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Groups': [
            {'Key': 'SubscriptionId', 'Value': '12121212121',
             'Attributes': {'accountId': '789456123012', 'accountName': 'payer', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:50:13.000Z',
                            'effectiveHourlyRate': '0.01210045700470754', 'endDateTime': '2024-12-05T18:50:13.000Z',
                            'hourlyRecurringFee': '0.0', 'instanceFamily': '', 'instanceType': 'db.t3.micro',
                                                    'leaseId': 'ri-2023-12-06-18-50-03-477', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:50:14.000Z',
                                                    'subscriptionId': '12121212121', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'All Upfront', 'tenancy': 'Shared', 'totalAssetValue': '106.0',
                                                    'upfrontFee': '106.0'},
             'Utilization': {'UtilizationPercentage': '100', 'PurchasedHours': '696', 'TotalActualHours': '696',
                             'UnusedHours': '0', 'OnDemandCostOfRIHoursUsed': '12.528', 'NetRISavings': '4.10608219',
                             'TotalPotentialRISavings': '4.10608219', 'AmortizedUpfrontFee': '8.42191781',
                             'AmortizedRecurringFee': '0', 'TotalAmortizedFee': '8.42191781',
                             'RICostForUnusedHours': '0', 'RealizedSavings': '4.10608219', 'UnrealizedSavings': '0'}},
            {'Key': 'SubscriptionId', 'Value': '13131313131',
             'Attributes': {'accountId': '789456123012', 'accountName': 'payer', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:50:53.000Z',
                            'effectiveHourlyRate': '0.012364383757115162', 'endDateTime': '2024-12-05T18:50:53.000Z',
                            'hourlyRecurringFee': '0.0062', 'instanceFamily': '', 'instanceType': 'db.t3.micro',
                            'leaseId': 'ri-2023-12-06-18-50-52-761', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-52-761',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:50:54.000Z',
                                                    'subscriptionId': '13131313131', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'Partial Upfront', 'tenancy': 'Shared',
                                                    'totalAssetValue': '108.31199827777778', 'upfrontFee': '54.0'},
             'Utilization': {'UtilizationPercentage': '100', 'PurchasedHours': '696', 'TotalActualHours': '696',
                             'UnusedHours': '0', 'OnDemandCostOfRIHoursUsed': '12.528', 'NetRISavings': '3.92238904',
                             'TotalPotentialRISavings': '3.92238904', 'AmortizedUpfrontFee': '4.29041096',
                             'AmortizedRecurringFee': '4.3152', 'TotalAmortizedFee': '8.60561096',
                             'RICostForUnusedHours': '0', 'RealizedSavings': '3.92238904', 'UnrealizedSavings': '0'}},
            {'Key': 'SubscriptionId', 'Value': '14141414141',
             'Attributes': {'accountId': '789456123012', 'accountName': 'payer', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:51:31.000Z', 'effectiveHourlyRate': '0.0129',
                            'endDateTime': '2024-12-05T18:51:31.000Z', 'hourlyRecurringFee': '0.0129',
                            'instanceFamily': '', 'instanceType': 'db.t3.micro',
                            'leaseId': 'ri-2023-12-06-18-51-29-735', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-51-29-735',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:51:32.000Z',
                                                    'subscriptionId': '14141414141', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'No Upfront', 'tenancy': 'Shared',
                                                    'totalAssetValue': '113.00399641666667', 'upfrontFee': '0.0'},
             'Utilization': {'UtilizationPercentage': '100', 'PurchasedHours': '696', 'TotalActualHours': '696',
                             'UnusedHours': '0', 'OnDemandCostOfRIHoursUsed': '12.528', 'NetRISavings': '3.5496',
                             'TotalPotentialRISavings': '3.5496', 'AmortizedUpfrontFee': '0',
                             'AmortizedRecurringFee': '8.9784', 'TotalAmortizedFee': '8.9784',
                             'RICostForUnusedHours': '0', 'RealizedSavings': '3.5496', 'UnrealizedSavings': '0'}}],
         'Total': {'UtilizationPercentage': '100', 'PurchasedHours': '2088.0', 'TotalActualHours': '2088.0',
                   'UnusedHours': '0.0', 'OnDemandCostOfRIHoursUsed': '37.584', 'NetRISavings': '11.5780712299999995',
                   'TotalPotentialRISavings': '11.5780712299999989', 'AmortizedUpfrontFee': '12.71232877',
                   'AmortizedRecurringFee': '13.293599999999999', 'TotalAmortizedFee': '26.005928769999999',
                   'RICostForUnusedHours': '0', 'RealizedSavings': '11.57807123', 'UnrealizedSavings': '0'}}],
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Fri, 08 Mar 2024 20:43:53 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4566',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_rds_usage.return_value = {'555555555555': Decimal(
        '696.0'), '444444444444': Decimal('2065.7187435')}
    actual = create_reserved_instances_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.reserved_instances.get_rds_normalized_hours_by_linked_account')
def test_create_reserved_instances_custom_line_items_for_commitment_purchased_in_billing_group(mock_rds_usage,
                                                                                               mock_client):
    expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_reservation_utilization.return_value = {'UtilizationsByTime': [
        {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Groups': [
            {'Key': 'SubscriptionId', 'Value': '12121212121',
             'Attributes': {'accountId': '789456123012', 'accountName': 'payer', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:50:13.000Z',
                            'effectiveHourlyRate': '0.01210045700470754', 'endDateTime': '2024-12-05T18:50:13.000Z',
                            'hourlyRecurringFee': '0.0', 'instanceFamily': '', 'instanceType': 'db.t3.micro',
                                                    'leaseId': 'ri-2023-12-06-18-50-03-477', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:50:14.000Z',
                                                    'subscriptionId': '12121212121', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'All Upfront', 'tenancy': 'Shared', 'totalAssetValue': '106.0',
                                                    'upfrontFee': '106.0'},
             'Utilization': {'UtilizationPercentage': '100', 'PurchasedHours': '696', 'TotalActualHours': '696',
                             'UnusedHours': '0', 'OnDemandCostOfRIHoursUsed': '12.528', 'NetRISavings': '4.10608219',
                             'TotalPotentialRISavings': '4.10608219', 'AmortizedUpfrontFee': '8.42191781',
                             'AmortizedRecurringFee': '0', 'TotalAmortizedFee': '8.42191781',
                             'RICostForUnusedHours': '0', 'RealizedSavings': '4.10608219', 'UnrealizedSavings': '0'}},
            {'Key': 'SubscriptionId', 'Value': '13131313131',
             'Attributes': {'accountId': '555555555555', 'accountName': 'General Sandbox', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:50:53.000Z',
                            'effectiveHourlyRate': '0.012364383757115162', 'endDateTime': '2024-12-05T18:50:53.000Z',
                            'hourlyRecurringFee': '0.0062', 'instanceFamily': '', 'instanceType': 'db.t3.micro',
                            'leaseId': 'ri-2023-12-06-18-50-52-761', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:555555555555:ri:ri-2023-12-06-18-50-52-761',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:50:54.000Z',
                                                    'subscriptionId': '13131313131', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'Partial Upfront', 'tenancy': 'Shared',
                                                    'totalAssetValue': '108.31199827777778', 'upfrontFee': '54.0'},
             'Utilization': {'UtilizationPercentage': '100', 'PurchasedHours': '696', 'TotalActualHours': '696',
                             'UnusedHours': '0', 'OnDemandCostOfRIHoursUsed': '12.528', 'NetRISavings': '3.92238904',
                             'TotalPotentialRISavings': '3.92238904', 'AmortizedUpfrontFee': '4.29041096',
                             'AmortizedRecurringFee': '4.3152', 'TotalAmortizedFee': '8.60561096',
                             'RICostForUnusedHours': '0', 'RealizedSavings': '3.92238904', 'UnrealizedSavings': '0'}}],
         'Total': {'UtilizationPercentage': '100', 'PurchasedHours': '1392.0', 'TotalActualHours': '1392.0',
                   'UnusedHours': '0.0', 'OnDemandCostOfRIHoursUsed': '25.056', 'NetRISavings': '8.02847123',
                   'TotalPotentialRISavings': '8.02847123', 'AmortizedUpfrontFee': '12.71232877',
                   'AmortizedRecurringFee': '4.3152', 'TotalAmortizedFee': '17.02752877',
                   'RICostForUnusedHours': '0', 'RealizedSavings': '8.02847123', 'UnrealizedSavings': '0'}}],
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Fri, 08 Mar 2024 20:43:53 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4566',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_rds_usage.return_value = {'555555555555': Decimal(
        '100'), '444444444444': Decimal('100')}
    actual = create_reserved_instances_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True)
    assert is_equal_list_of_dict(actual, expected)


@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.reserved_instances.get_rds_normalized_hours_by_linked_account')
def test_create_reserved_instances_custom_line_items_for_negative_net_savings(mock_rds_usage,
                                                                              mock_client):
    expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
                 'AccountId': '444444444444'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
                 'AccountId': '555555555555'}]
    mock_client().get_reservation_utilization.return_value = {'UtilizationsByTime': [
        {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Groups': [
            {'Key': 'SubscriptionId', 'Value': '12121212121',
             'Attributes': {'accountId': '789456123012', 'accountName': 'payer', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:50:13.000Z',
                            'effectiveHourlyRate': '0.01210045700470754', 'endDateTime': '2024-12-05T18:50:13.000Z',
                            'hourlyRecurringFee': '0.0', 'instanceFamily': '', 'instanceType': 'db.t3.micro',
                                                    'leaseId': 'ri-2023-12-06-18-50-03-477', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:50:14.000Z',
                                                    'subscriptionId': '12121212121', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'All Upfront', 'tenancy': 'Shared', 'totalAssetValue': '106.0',
                                                    'upfrontFee': '106.0'},
             'Utilization': {'UtilizationPercentage': '0', 'PurchasedHours': '696', 'TotalActualHours': '0',
                             'UnusedHours': '696', 'OnDemandCostOfRIHoursUsed': '0', 'NetRISavings': '-4.10608219',
                             'TotalPotentialRISavings': '4.10608219', 'AmortizedUpfrontFee': '8.42191781',
                             'AmortizedRecurringFee': '0', 'TotalAmortizedFee': '8.42191781',
                             'RICostForUnusedHours': '4.10608219', 'RealizedSavings': '-4.10608219',
                                                     'UnrealizedSavings': '4.10608219'}}],
         'Total': {'UtilizationPercentage': '0', 'PurchasedHours': '1392.0', 'TotalActualHours': '0',
                   'UnusedHours': '1392.0', 'OnDemandCostOfRIHoursUsed': '0', 'NetRISavings': '-8.02847123',
                   'TotalPotentialRISavings': '8.02847123', 'AmortizedUpfrontFee': '12.71232877',
                   'AmortizedRecurringFee': '4.3152', 'TotalAmortizedFee': '17.02752877',
                   'RICostForUnusedHours': '8.02847123', 'RealizedSavings': '-8.02847123',
                   'UnrealizedSavings': '8.028471230'}}],
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Fri, 08 Mar 2024 20:43:53 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4566',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_rds_usage.return_value = {'555555555555': Decimal(
        '100'), '444444444444': Decimal('100')}
    actual = create_reserved_instances_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True)
    assert is_equal_list_of_dict(actual, expected)



@mock.patch('boto3.client')
@mock.patch('sam_sp_ri_utility.services.reserved_instances.get_rds_normalized_hours_by_linked_account')
def test_create_reserved_instances_custom_line_items_for_standard_input_specify_subscription_ids(mock_rds_usage, mock_client):
    expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-51-29-735-Account-444444444444-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-51-29-735 for 444444444444 based on 74.80% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 2.655040550086921}, 'Type': 'CREDIT'},
                 'AccountId': '444444444444'},
                {'Name': 'ReservedInstance-ri-2023-12-06-18-51-29-735-Account-555555555555-Benefit-2024-02-01',
                 'Description': 'Credit from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-51-29-735 for 555555555555 based on 25.20% of RDS normalized instance hours',
                 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
                 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
                                        'ExclusiveEndBillingPeriod': '2024-03'},
                 'ChargeDetails': {'Flat': {'ChargeValue': 0.8945594499130791}, 'Type': 'CREDIT'},
                 'AccountId': '555555555555'}]
    mock_client().get_reservation_utilization.return_value = {'UtilizationsByTime': [
        {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Groups': [
            {'Key': 'SubscriptionId', 'Value': '14141414141',
             'Attributes': {'accountId': '789456123012', 'accountName': 'payer', 'availabilityZone': '',
                            'averageOnDemandHourlyRate': '0.018000000000000002',
                            'cancellationDateTime': '2024-12-05T18:51:31.000Z', 'effectiveHourlyRate': '0.0129',
                            'endDateTime': '2024-12-05T18:51:31.000Z', 'hourlyRecurringFee': '0.0129',
                            'instanceFamily': '', 'instanceType': 'db.t3.micro',
                            'leaseId': 'ri-2023-12-06-18-51-29-735', 'modificationStatus': 'Not Manual',
                                                    'numberOfInstances': '1', 'offeringType': '', 'platform': 'PostgreSQL',
                                                    'region': 'us-west-2',
                                                    'reservationARN': 'arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-51-29-735',
                                                    'scope': 'Region', 'service': 'Amazon Relational Database Service',
                                                    'sizeFlexibility': 'FlexRI', 'startDateTime': '2023-12-06T18:51:32.000Z',
                                                    'subscriptionId': '14141414141', 'subscriptionStatus': 'Active',
                                                    'subscriptionType': 'No Upfront', 'tenancy': 'Shared',
                                                    'totalAssetValue': '113.00399641666667', 'upfrontFee': '0.0'},
             'Utilization': {'UtilizationPercentage': '100', 'PurchasedHours': '696', 'TotalActualHours': '696',
                             'UnusedHours': '0', 'OnDemandCostOfRIHoursUsed': '12.528', 'NetRISavings': '3.5496',
                             'TotalPotentialRISavings': '3.5496', 'AmortizedUpfrontFee': '0',
                             'AmortizedRecurringFee': '8.9784', 'TotalAmortizedFee': '8.9784',
                             'RICostForUnusedHours': '0', 'RealizedSavings': '3.5496', 'UnrealizedSavings': '0'}}],
         'Total': {'UtilizationPercentage': '100', 'PurchasedHours': '2088.0', 'TotalActualHours': '2088.0',
                   'UnusedHours': '0.0', 'OnDemandCostOfRIHoursUsed': '37.584', 'NetRISavings': '11.5780712299999995',
                   'TotalPotentialRISavings': '11.5780712299999989', 'AmortizedUpfrontFee': '12.71232877',
                   'AmortizedRecurringFee': '13.293599999999999', 'TotalAmortizedFee': '26.005928769999999',
                   'RICostForUnusedHours': '0', 'RealizedSavings': '11.57807123', 'UnrealizedSavings': '0'}}],
        'ResponseMetadata': {
        'RequestId': '8a94e821-2206-439b-9267-3856ff64203e',
        'HTTPStatusCode': 200, 'HTTPHeaders': {
            'date': 'Fri, 08 Mar 2024 20:43:53 GMT',
            'content-type': 'application/x-amz-json-1.1',
            'content-length': '4566',
            'connection': 'keep-alive',
                            'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                            'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    mock_client().list_account_associations.return_value = default_account_associations_response
    mock_rds_usage.return_value = {'555555555555': Decimal(
        '696.0'), '444444444444': Decimal('2065.7187435')}
    actual = create_reserved_instances_custom_line_items(
        date(2024, 2, 1), date(2024, 3, 1), True, '14141414141')
    assert is_equal_list_of_dict(actual, expected)