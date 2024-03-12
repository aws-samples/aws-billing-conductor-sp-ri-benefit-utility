from sam_sp_ri_utility.services.usage import *
from unittest import mock


@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_period_with_no_usage(mock_client):
    expected = {}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2021-02-01', 'End': '2021-03-01'},
             'Total': {'UsageQuantity': {'Amount': '0', 'Unit': 'N/A'}}, 'Groups': [], 'Estimated': True}],
         'DimensionValueAttributes': [],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:06:50 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '294',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2021-02-01', '2021-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_standard_input(mock_client):
    expected = {'123456789012': Decimal(
        '7656'), '210978654321': Decimal('4872')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}],
         'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'},
             'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-BoxUsage:m5.large'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-BoxUsage:t3.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-BoxUsage:t4g.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '696', 'Unit': 'Hrs'}}},
                {'Keys': ['210978654321', 'USW2-BoxUsage:m5.large'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '696', 'Unit': 'Hrs'}}},
                {'Keys': ['210978654321', 'USW2-BoxUsage:t3.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
                {'Keys': ['210978654321', 'USW2-BoxUsage:t3a.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '696', 'Unit': 'Hrs'}}}],
             'Estimated': False}], 'DimensionValueAttributes': [
            {'Value': '123456789012', 'Attributes': {
                'description': 'Secondary Sandbox'}},
            {'Value': '210978654321', 'Attributes': {'description': 'General Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                              'HTTPHeaders': {
                                  'date': 'Thu, 07 Mar 2024 20:36:01 GMT',
                                  'content-type': 'application/x-amz-json-1.1',
                                  'content-length': '1056',
                                  'connection': 'keep-alive',
                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                  'cache-control': 'no-cache'},
                              'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_unused_odcrs(mock_client):
    expected = {'123456789012': Decimal('1392')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}],
         'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'},
             'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-BoxUsage:t3.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-UnusedBox:t4g.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '696', 'Unit': 'Hrs'}}}],
             'Estimated': False}], 'DimensionValueAttributes': [
            {'Value': '123456789012', 'Attributes': {
                'description': 'Secondary Sandbox'}},
            {'Value': '210978654321', 'Attributes': {'description': 'General Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                              'HTTPHeaders': {
                                  'date': 'Thu, 07 Mar 2024 20:36:01 GMT',
                                  'content-type': 'application/x-amz-json-1.1',
                                  'content-length': '1056',
                                  'connection': 'keep-alive',
                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                  'cache-control': 'no-cache'},
                              'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_unused_dedicated_hosts(mock_client):
    expected = {'123456789012': Decimal('1392')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}],
         'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'},
             'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-BoxUsage:t3.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-UnusedDed:c6gd.12xlarge'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '696', 'Unit': 'Hrs'}}}],
             'Estimated': False}], 'DimensionValueAttributes': [
            {'Value': '123456789012', 'Attributes': {
                'description': 'Secondary Sandbox'}},
            {'Value': '210978654321', 'Attributes': {'description': 'General Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                              'HTTPHeaders': {
                                  'date': 'Thu, 07 Mar 2024 20:36:01 GMT',
                                  'content-type': 'application/x-amz-json-1.1',
                                  'content-length': '1056',
                                  'connection': 'keep-alive',
                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                  'cache-control': 'no-cache'},
                              'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


# the expected behavior is that shared and dedicated tenancy usage uses the same normalization factor
# this causes shared and dedicated usage to be equivalent, where we know that dedicated pricing is higher than shared
# the higher cost could mean lower coverage in the consolidated bill (i.e., what you pay to AWS) in real usage
# in this model, this effect would not happen
# assuming that shared and dedicated have the same SP discount over On-Demand, they would receive equivalent coverage
# open an issue if you think this should be changed by default
@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_dedicated_hosts(mock_client):
    expected = {'123456789012': Decimal('2784')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}],
         'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'},
             'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-DedicatedUsage:m5.large'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '696', 'Unit': 'Hrs'}}}],
             'Estimated': False}], 'DimensionValueAttributes': [
            {'Value': '123456789012', 'Attributes': {
                'description': 'Secondary Sandbox'}},
            {'Value': '210978654321', 'Attributes': {'description': 'General Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                              'HTTPHeaders': {
                                  'date': 'Thu, 07 Mar 2024 20:36:01 GMT',
                                  'content-type': 'application/x-amz-json-1.1',
                                  'content-length': '1056',
                                  'connection': 'keep-alive',
                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                  'cache-control': 'no-cache'},
                              'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_unmatched_instance_size_normalization(mock_client):
    expected = {'123456789012': Decimal('1300')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}],
         'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'},
             'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-BoxUsage:m5.metal'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1300', 'Unit': 'Hrs'}}}],
             'Estimated': False}], 'DimensionValueAttributes': [
            {'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                              'HTTPHeaders': {
                                  'date': 'Thu, 07 Mar 2024 20:36:01 GMT',
                                  'content-type': 'application/x-amz-json-1.1',
                                  'content-length': '1056',
                                  'connection': 'keep-alive',
                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                  'cache-control': 'no-cache'},
                              'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_ec2_normalized_hours_by_linked_account_for_spot_usage(mock_client):
    expected = {'123456789012': Decimal('1392')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}],
         'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'},
             'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-SpotUsage:m5.xlarge'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1300', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-BoxUsage:t3.small'],
                 'Metrics': {
                    'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
            ],
                'Estimated': False}], 'DimensionValueAttributes': [
            {'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                              'HTTPHeaders': {
                                  'date': 'Thu, 07 Mar 2024 20:36:01 GMT',
                                  'content-type': 'application/x-amz-json-1.1',
                                  'content-length': '1056',
                                  'connection': 'keep-alive',
                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                  'cache-control': 'no-cache'},
                              'RetryAttempts': 0}}
    actual = get_ec2_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_fargate_vcpu_hours_by_linked_account_for_period_with_no_usage(mock_client):
    expected = {}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2021-02-01', 'End': '2021-03-01'},
             'Total': {'UsageQuantity': {'Amount': '0', 'Unit': 'N/A'}}, 'Groups': [], 'Estimated': True}],
         'DimensionValueAttributes': [],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:12:24 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '294',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_fargate_vcpu_hours_by_linked_account(
        '2021-02-01', '2021-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_fargate_vcpu_hours_by_linked_account_for_standard_input(mock_client):
    expected = {'123456789012': Decimal('2784.1389044444')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-DataTransfer-Regional-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.1370846155', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USW2-Fargate-GB-Hours'],
                 'Metrics': {'UsageQuantity': {'Amount': '8352.4167133334', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-Fargate-vCPU-Hours:perCPU'],
                 'Metrics': {'UsageQuantity': {'Amount': '2784.1389044444', 'Unit': 'Hrs'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:13:44 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '700',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_fargate_vcpu_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_fargate_vcpu_hours_by_linked_account_for_spot_usage(mock_client):
    expected = {'123456789012': Decimal('2784.1389044444')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-DataTransfer-Regional-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.1370846155', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USW2-Fargate-GB-Hours'],
                 'Metrics': {'UsageQuantity': {'Amount': '8352.4167133334', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-SpotUsage-Fargate-vCPU-Hours:perCPU'],
                 'Metrics': {'UsageQuantity': {'Amount': '320.1233321', 'Unit': 'Hrs'}}},
                {'Keys': ['123456789012', 'USW2-Fargate-vCPU-Hours:perCPU'],
                 'Metrics': {'UsageQuantity': {'Amount': '2784.1389044444', 'Unit': 'Hrs'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:13:44 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '700',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_fargate_vcpu_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_lambda_gb_hours_by_linked_account_for_period_with_no_usage(mock_client):
    expected = {}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2021-02-01', 'End': '2021-03-01'},
             'Total': {'UsageQuantity': {'Amount': '0', 'Unit': 'N/A'}}, 'Groups': [], 'Estimated': True}],
         'DimensionValueAttributes': [],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:22:23 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '294',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_lambda_gb_hours_by_linked_account('2021-02-01', '2021-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_lambda_gb_hours_by_linked_account_for_standard_input(mock_client):
    expected = {'123456789012': Decimal('0.01976340277777777777777777777'),
                '210987654321': Decimal('2.901497847222222222222222222')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'Lambda-GB-Second'],
                 'Metrics': {'UsageQuantity': {'Amount': '65.675375', 'Unit': 'Second'}}},
                {'Keys': ['123456789012', 'Lambda-GB-Second-ARM'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.7825', 'Unit': 'Lambda-GB-Second'}}},
                {'Keys': ['123456789012', 'Request'],
                 'Metrics': {'UsageQuantity': {'Amount': '77', 'Unit': 'Requests'}}},
                {'Keys': ['123456789012', 'Request-ARM'],
                 'Metrics': {'UsageQuantity': {'Amount': '1', 'Unit': 'Requests'}}},
                {'Keys': ['123456789012', 'USE1-CloudFront-In-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0000144523', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USE1-CloudFront-Out-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0000057891', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USW2-CloudFront-In-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0000664461', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USW2-CloudFront-Out-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0000874735', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USW2-Lambda-GB-Second-ARM'],
                 'Metrics': {'UsageQuantity': {'Amount': '4.690375', 'Unit': 'Lambda-GB-Second'}}},
                {'Keys': ['123456789012', 'USW2-Request-ARM'],
                 'Metrics': {'UsageQuantity': {'Amount': '3', 'Unit': 'Requests'}}},
                {'Keys': ['123456789012', 'USW2-USE1-AWS-In-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0001553353', 'Unit': 'GB'}}},
                {'Keys': ['123456789012', 'USW2-USE1-AWS-Out-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.000065919', 'Unit': 'GB'}}},
                {'Keys': ['210987654321', 'USW2-Lambda-GB-Second-ARM'],
                 'Metrics': {'UsageQuantity': {'Amount': '10445.39225', 'Unit': 'Lambda-GB-Second'}}},
                {'Keys': ['210987654321', 'USW2-Request-ARM'],
                 'Metrics': {'UsageQuantity': {'Amount': '705', 'Unit': 'Requests'}}},
                {'Keys': ['210987654321', 'USW2-USE1-AWS-In-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0003147963', 'Unit': 'GB'}}},
                {'Keys': ['210987654321', 'USW2-USE1-AWS-Out-Bytes'],
                 'Metrics': {'UsageQuantity': {'Amount': '0.0001272597', 'Unit': 'GB'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'scottie-enriquez'}},
                                      {'Value': '210987654321', 'Attributes': {'description': 'General Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:23:37 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '2253',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_lambda_gb_hours_by_linked_account('2021-02-01', '2021-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_rds_normalized_hours_by_linked_account_for_period_with_no_usage(mock_client):
    expected = {}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2021-02-01', 'End': '2021-03-01'},
             'Total': {'UsageQuantity': {'Amount': '0', 'Unit': 'N/A'}}, 'Groups': [], 'Estimated': True}],
         'DimensionValueAttributes': [],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:29:20 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '294',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_rds_normalized_hours_by_linked_account(
        '2021-02-01', '2021-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_rds_normalized_hours_by_linked_account_for_standard_input(mock_client):
    expected = {'123456789012': Decimal(
        '696.0'), '210987654321': Decimal('2065.7187435')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-InstanceUsage:db.t3.micro'],
                 'Metrics': {'UsageQuantity': {'Amount': '1392', 'Unit': 'Hrs'}}},
                {'Keys': ['210987654321', 'USW2-InstanceUsage:db.r5.large'],
                 'Metrics': {'UsageQuantity': {'Amount': '138.189443', 'Unit': 'Hrs'}}},
                {'Keys': ['210987654321', 'USW2-InstanceUsage:db.t3.micro'],
                 'Metrics': {'UsageQuantity': {'Amount': '833.921943', 'Unit': 'Hrs'}}},
                {'Keys': ['210987654321', 'USW2-InstanceUsageIOOptimized:db.r5.large'],
                 'Metrics': {'UsageQuantity': {'Amount': '274', 'Unit': 'Hrs'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}},
                                      {'Value': '210987654321', 'Attributes': {'description': 'General Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:32:02 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '890',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_rds_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_rds_normalized_hours_by_linked_account_for_xlarge_normalization(mock_client):
    expected = {'123456789012': Decimal('6400')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'InstanceUsage:db.r6g.8xl'],
                 'Metrics': {'UsageQuantity': {'Amount': '100', 'Unit': 'Hrs'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:32:02 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '890',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_rds_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_rds_normalized_hours_by_linked_account_for_multi_az(mock_client):
    expected = {'123456789012': Decimal('6400')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USE2-Multi-AZUsage:db.r6g.4xl'],
                 'Metrics': {'UsageQuantity': {'Amount': '100', 'Unit': 'Hrs'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:32:02 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '890',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_rds_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected


@mock.patch('boto3.client')
def test_get_rds_normalized_hours_by_linked_account_for_multi_az_cluster(mock_client):
    expected = {'123456789012': Decimal('1200')}
    mock_client().get_cost_and_usage.return_value = \
        {'GroupDefinitions': [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'},
                              {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}], 'ResultsByTime': [
            {'TimePeriod': {'Start': '2024-02-01', 'End': '2024-03-01'}, 'Total': {}, 'Groups': [
                {'Keys': ['123456789012', 'USW2-Multi-AZClusterUsage:db.m5d.large'],
                 'Metrics': {'UsageQuantity': {'Amount': '100', 'Unit': 'Hrs'}}}], 'Estimated': False}],
         'DimensionValueAttributes': [{'Value': '123456789012', 'Attributes': {'description': 'Secondary Sandbox'}}],
         'ResponseMetadata': {'RequestId': '8a94e821-2206-439b-9267-3856ff64203e', 'HTTPStatusCode': 200,
                                  'HTTPHeaders': {'date': 'Thu, 07 Mar 2024 21:32:02 GMT',
                                                  'content-type': 'application/x-amz-json-1.1', 'content-length': '890',
                                                  'connection': 'keep-alive',
                                                  'x-amzn-requestid': '8a94e821-2206-439b-9267-3856ff64203e',
                                                  'cache-control': 'no-cache'}, 'RetryAttempts': 0}}
    actual = get_rds_normalized_hours_by_linked_account(
        '2024-02-01', '2024-03-01')
    assert actual == expected
