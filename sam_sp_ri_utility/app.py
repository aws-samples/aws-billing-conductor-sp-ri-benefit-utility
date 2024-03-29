import datetime
import json
import os
from services import savings_plans, reserved_instances


def lambda_handler(event, context):
    is_dry_run = os.environ.get('DRY_RUN', 'Enabled') == 'Enabled'
    include_fargate_for_savings_plans = os.environ.get(
        'INCLUDE_FARGATE_FOR_SAVINGS_PLANS', 'Disabled') == 'Enabled'
    include_lambda_for_savings_plans = os.environ.get(
        'INCLUDE_LAMBDA_FOR_SAVINGS_PLANS', 'Disabled') == 'Enabled'
    today = datetime.datetime.today()
    # first day of the previous month
    inclusive_start_billing_period = (
        today - datetime.timedelta(today.day)).replace(day=1)
    # first day of the current month
    exclusive_end_billing_period = today.replace(day=1)
    reserved_instances_custom_line_items = reserved_instances.create_reserved_instances_custom_line_items(
        inclusive_start_billing_period, exclusive_end_billing_period, is_dry_run)
    savings_plans_custom_line_items = savings_plans.create_savings_plans_custom_line_items(
        inclusive_start_billing_period, exclusive_end_billing_period, is_dry_run, include_fargate_for_savings_plans,
        include_lambda_for_savings_plans)
    return {
        "lineItems": json.dumps({
            "reservedInstancesCustomLineItems": reserved_instances_custom_line_items,
            "savingsPlansCustomLineItems": savings_plans_custom_line_items
        })
    }
