from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


scenarios('../features/filter_and_sort_cases.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@given('Queue has been created')
def create_queue(driver, register_organisation, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.add_queue(context)
    api.assign_case_to_queue(context)
