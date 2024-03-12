import boto3
from decimal import *

# https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/apply_ri.html
# additional items could be added for bare metal instances
# .metal instance sizes do not have a single normalization factor
# they vary based on the specific instance family
# https://docs.aws.amazon.com/whitepapers/latest/cost-optimization-reservation-models/normalization-factor-for-bare-metal-instances.html
size_normalization_factor_map = {
	'nano': Decimal(0.25),
	'micro': Decimal(0.50),
	'small': Decimal(1.0),
	'medium': Decimal(2.0),
	'large': Decimal(4.0),
	'xlarge': Decimal(8.0),
	'2xlarge': Decimal(16.0),
	'3xlarge': Decimal(24.0),
	'4xlarge': Decimal(32.0),
	'6xlarge': Decimal(48.0),
	'8xlarge': Decimal(64.0),
	'9xlarge': Decimal(72.0),
	'10xlarge': Decimal(80.0),
	'12xlarge': Decimal(96.0),
	'16xlarge': Decimal(128.0),
	'18xlarge': Decimal(144.0),
	'24xlarge': Decimal(192.0),
	'32xlarge': Decimal(256.0),
	'48xlarge': Decimal(384.0),
	'56xlarge': Decimal(448.0),
	'112xlarge': Decimal(896.0)
}


def get_ec2_normalized_hours_by_linked_account(start_date_string, end_date_string):
	cost_explorer_client = boto3.client('ce')
	time_period = {'Start': start_date_string, 'End': end_date_string}
	filter = {'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['EC2: Running Hours']}}
	group_by = [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}]
	ec2_cost_and_usage_data = cost_explorer_client.get_cost_and_usage(
		TimePeriod=time_period,
		Granularity='MONTHLY',
		Filter=filter,
		Metrics=['UsageQuantity'],
		GroupBy=group_by
	).get('ResultsByTime', [])[0].get('Groups', [])
	normalized_instance_hours_by_linked_account = {}
	for row in ec2_cost_and_usage_data:
		linked_account = row.get('Keys')[0]
		usage_type = row.get('Keys')[1]
		# an example Spot usage type is USW2-SpotUsage:m5.xlarge
		# an example usage type for unused ODCRs is USW2-UnusedBox:c6g.xlarge
		# an example usage type for an unused dedicated host is USW2-UnusedDed:c6gd.12xlarge
		if 'SpotUsage' not in usage_type and 'Unused' not in usage_type:
			running_hours = Decimal(row.get('Metrics').get('UsageQuantity').get('Amount'))
			# an example usage type is USW1-BoxUsage:c5.2xlarge
			instance_size = usage_type.split(':')[1].split('.')[1]
			normalized_instance_hours = running_hours * size_normalization_factor_map.get(instance_size, Decimal(1.0))
			if linked_account in normalized_instance_hours_by_linked_account:
				normalized_instance_hours_by_linked_account[linked_account] += normalized_instance_hours
			else:
				normalized_instance_hours_by_linked_account[linked_account] = normalized_instance_hours
	return normalized_instance_hours_by_linked_account


def get_fargate_vcpu_hours_by_linked_account(start_date_string, end_date_string):
	cost_explorer_client = boto3.client('ce')
	time_period = {'Start': start_date_string, 'End': end_date_string}
	filter = {'Dimensions': {'Key': 'OPERATION', 'Values': ['FargateTask']}}
	group_by = [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}]
	fargate_cost_and_usage_data = cost_explorer_client.get_cost_and_usage(
		TimePeriod=time_period,
		Granularity='MONTHLY',
		Filter=filter,
		Metrics=['UsageQuantity'],
		GroupBy=group_by
	).get('ResultsByTime')[0].get('Groups')
	vcpu_hours_by_linked_account = {}
	for row in fargate_cost_and_usage_data:
		linked_account = row.get('Keys')[0]
		usage_type = row.get('Keys')[1]
		if 'Fargate-vCPU-Hours:perCPU' in usage_type and 'Spot' not in usage_type:
			vcpu_hours = Decimal(row.get('Metrics').get('UsageQuantity').get('Amount'))
			if linked_account in vcpu_hours_by_linked_account:
				vcpu_hours_by_linked_account[linked_account] += vcpu_hours
			else:
				vcpu_hours_by_linked_account[linked_account] = vcpu_hours
	return vcpu_hours_by_linked_account


def get_lambda_gb_hours_by_linked_account(start_date_string, end_date_string):
	cost_explorer_client = boto3.client('ce')
	time_period = {'Start': start_date_string, 'End': end_date_string}
	filter = {'Dimensions': {'Key': 'OPERATION', 'Values': ['Invoke']}}
	group_by = [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}]
	lambda_cost_and_usage_data = cost_explorer_client.get_cost_and_usage(
		TimePeriod=time_period,
		Granularity='MONTHLY',
		Filter=filter,
		Metrics=['UsageQuantity'],
		GroupBy=group_by
	).get('ResultsByTime')[0].get('Groups')
	gb_hours_by_linked_account = {}
	for row in lambda_cost_and_usage_data:
		linked_account = row.get('Keys')[0]
		usage_type = row.get('Keys')[1]
		if 'Lambda-GB-Second' in usage_type:
			gb_hours = Decimal(row.get('Metrics').get('UsageQuantity').get('Amount')) / Decimal(3600.0)
			if linked_account in gb_hours_by_linked_account:
				gb_hours_by_linked_account[linked_account] += gb_hours
			else:
				gb_hours_by_linked_account[linked_account] = gb_hours
	return gb_hours_by_linked_account


def get_rds_normalized_hours_by_linked_account(start_date_string, end_date_string):
	cost_explorer_client = boto3.client('ce')
	time_period = {'Start': start_date_string, 'End': end_date_string}
	filter = {'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['RDS: Running Hours']}}
	group_by = [{'Type': 'DIMENSION', 'Key': 'LINKED_ACCOUNT'}, {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}]
	rds_cost_and_usage_data = cost_explorer_client.get_cost_and_usage(
		TimePeriod=time_period,
		Granularity='MONTHLY',
		Filter=filter,
		Metrics=['UsageQuantity'],
		GroupBy=group_by
	).get('ResultsByTime')[0].get('Groups')
	normalized_instance_hours_by_linked_account = {}
	for row in rds_cost_and_usage_data:
		linked_account = row.get('Keys')[0]
		usage_type = row.get('Keys')[1]
		# an example usage type is USW2-Multi-AZUsage:db.m5.xl
		instance_size = usage_type.split(':')[1].split('.')[2]
		# convert usage type size to size format in normalization table
		if instance_size.endswith('xl'):
			instance_size = instance_size.replace('xl', 'xlarge')
		multi_az_factor = Decimal(1.0)
		# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html
		if 'Multi-AZCluster' in usage_type:
			multi_az_factor = Decimal(3)
		elif 'Multi-AZ' in usage_type:
			multi_az_factor = Decimal(2)
		running_hours = Decimal(row.get('Metrics').get('UsageQuantity').get('Amount'))
		normalized_instance_hours = running_hours * size_normalization_factor_map.get(instance_size,
																					  Decimal(1.0)) * multi_az_factor
		if linked_account in normalized_instance_hours_by_linked_account:
			normalized_instance_hours_by_linked_account[linked_account] += normalized_instance_hours
		else:
			normalized_instance_hours_by_linked_account[linked_account] = normalized_instance_hours
	return normalized_instance_hours_by_linked_account
