from pytest_bdd import given, when, then, parsers, scenarios
from selenium.webdriver.support.ui import Select
from helpers.helpers import get_formatted_date_time_m_d_h_s
from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr


scenarios('../features/filter_and_sort_cases.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@given('queue has been created')
def create_queue(register_organisation, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.add_queue('queue' + get_formatted_date_time_m_d_h_s())


@when('case has been moved to new Queue')
def assign_case_to_queue(context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == len(driver.find_elements_by_css_selector('.lite-cases-table .lite-cases-table-row'))


@when(parsers.parse('filter status has been changed to "{status}"'))
def filter_status_change(driver, context, status):
    select = Select(driver.find_element_by_id('status'))
    select.select_by_visible_text(status)
    driver.find_element_by_id("button-apply-filters").click()


@when(parsers.parse('Filter case type has been changed to "{case_type}"'))
def filter_status_change(driver, context, case_type):
    select = Select(driver.find_element_by_id('case_type'))
    select.select_by_visible_text(case_type)
    driver.find_element_by_id("button-apply-filters").click()


@when('I show filters')
def i_show_filters(driver, context):
    driver.find_element_by_id('show-filters-link').click()


@when('I click clear filters')
def i_show_filters(driver, context):
    driver.find_element_by_id('button-clear-filters').click()


@when('I hide filters')
def i_hide_filters(driver, context):
    driver.find_element_by_id('hide-filters-link').click()


@when(parsers.parse('I sort cases by "{sort_type}"'))
def i_sort_cases_by(driver, context, sort_type):
    driver.find_element_by_link_text(sort_type).click()


@when(parsers.parse('the cases are in order of "{sort_type}"'))
def the_cases_are_in_order_of(driver, context, sort_type):
    if sort_type == 'Status':
        rows = driver.find_elements_by_css_selector('lite-cases-table-row')
        assert rows[0].find_element_by_css_selector('p:last-child').text == 'Submitted'
        assert rows[1].find_element_by_css_selector('p:last-child').text == 'Under review'
    else:
        raise NotImplementedError


@when('the filters are no longer shown')
def the_filters_are_no_longer_shown(driver, context):
    assert not driver.find_element_by_class_name('lite-filter-bar--horizontal').is_displayed()
