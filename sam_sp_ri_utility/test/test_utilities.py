from .utilities import *


def test_is_equal_list_of_dict_for_same_list():
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
	actual = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
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
	assert is_equal_list_of_dict(expected, actual)


def test_is_equal_list_of_dict_for_same_list_different_order():
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
	actual = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
			   'AccountId': '555555555555'},
			  {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
			   'AccountId': '444444444444'}]
	assert is_equal_list_of_dict(expected, actual)


def test_is_equal_list_of_dict_for_different_value_in_first_list():
	expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
				 'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
				 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
				 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
										'ExclusiveEndBillinPeriod': '2024-03'},
				 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
				 'AccountId': '444444444444'},
				{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
				 'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
				 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
				 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
										'ExclusiveEndBillingPeriod': '2024-03'},
				 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
				 'AccountId': '555555555555'}]
	actual = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.05304109}, 'Type': 'FEE'},
			   'AccountId': '555555555555'},
			  {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
			   'AccountId': '444444444444'}]
	assert not is_equal_list_of_dict(expected, actual)


def test_is_equal_list_of_dict_for_different_value_in_second_list():
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
	actual = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.05304109}, 'Type': 'FEE'},
			   'AccountId': '555555555555'},
			  {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
			   'AccountId': '444444444444'}]
	assert not is_equal_list_of_dict(expected, actual)


def test_is_equal_list_of_dict_for_different_length_lists():
	expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
				 'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
				 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
				 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
										'ExclusiveEndBillingPeriod': '2024-03'},
				 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
				 'AccountId': '444444444444'}]
	actual = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-555555555555-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 555555555555 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/999999999999',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
			   'AccountId': '555555555555'},
			  {'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
			   'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
			   'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
			   'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
									  'ExclusiveEndBillingPeriod': '2024-03'},
			   'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
			   'AccountId': '444444444444'}]
	assert not is_equal_list_of_dict(expected, actual)


def test_is_equal_list_of_dict_for_one_empty_list():
	expected = [{'Name': 'ReservedInstance-ri-2023-12-06-18-50-03-477-Account-444444444444-Benefit-2024-02-01',
				 'Description': 'Fee from arn:aws:rds:us-west-2:789456123012:ri:ri-2023-12-06-18-50-03-477 for 444444444444 based on 50.00% of RDS normalized instance hours',
				 'BillingGroupArn': 'arn:aws:billingconductor::789456123012:billinggroup/888888888888',
				 'BillingPeriodRange': {'InclusiveStartBillingPeriod': '2024-02',
										'ExclusiveEndBillingPeriod': '2024-03'},
				 'ChargeDetails': {'Flat': {'ChargeValue': 2.053041095}, 'Type': 'FEE'},
				 'AccountId': '444444444444'}]
	actual = []
	assert not is_equal_list_of_dict(expected, actual)


def test_is_equal_list_of_dict_for_two_empty_lists():
	expected = []
	actual = []
	assert is_equal_list_of_dict(expected, actual)
