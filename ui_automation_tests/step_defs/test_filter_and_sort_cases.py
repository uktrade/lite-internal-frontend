from pytest_bdd import scenarios, given, when, then, parsers, scenarios

from helpers.helpers import get_formatted_date_time_m_d_h_s
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


scenarios('../features/filter_and_sort_cases.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@given('Queue has been created')
def create_queue(register_organisation, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.add_queue('queue' + get_formatted_date_time_m_d_h_s())


@when('Case has been moved to new Queue')
def assign_case_to_queue(context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == len(driver.find_elements_by_css_selector('.lite-cases-table .lite-cases-table-row'))


@when(parsers.parse('Filter status has been changed to "{approved}"'))
def filter_approved(driver, context, number):
    assert int(number) == len(driver.find_elements_by_css_selector('.lite-cases-table .lite-cases-table-row'))


@when('I show filters')
def i_show_filters(driver, context):
    driver.find_element_by_id('show-filters-link').click()


@when('I hide filters')
def i_hide_filters(driver, context):
    driver.find_element_by_id('hide-filters-link').click()

