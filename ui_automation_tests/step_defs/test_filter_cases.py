from pytest_bdd import given, when, then, parsers, scenarios

from pages.queues_pages import QueuesPages
from pages.shared import Shared
from shared.tools.wait import wait_until_page_is_loaded
from ui_automation_tests.pages.case_list_page import CaseListPage

scenarios("../features/filter_cases.feature", strict_gherkin=False)


@when("case has been moved to new Queue")
def assign_case_to_queue_when(api_test_client):
    api_test_client.cases.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == Shared(driver).get_number_of_rows_in_lite_table(), "incorrect number of cases are shown"


@when("I click clear filters")
def i_show_filters(driver, context):
    CaseListPage(driver).click_clear_filters_button()


@when("I hide filters")
def i_hide_filters(driver, context):
    CaseListPage(driver).click_hide_filters_link()


@then("the filters are shown")
def the_filters_are_shown(driver, context):
    assert CaseListPage(driver).is_filters_visible(), "filters are not shown"


@then("there are no cases shown")  # noqa
def no_cases_shown(driver):
    assert QueuesPages(driver).is_no_cases_notice_displayed(), "There are cases shown in the newly created queue."


@when(parsers.parse('filter case type has been changed to "{case_type}"'))  # noqa
def filter_status_change(driver, context, case_type):  # noqa
    CaseListPage(driver).select_filter_case_type_from_dropdown(case_type)
    CaseListPage(driver).click_apply_filters_button()


@when("I click filter to show cases with open team ecju queries")  # noqa
def i_show_filters(driver, context):  # noqa
    CaseListPage(driver).click_checkbox_to_show_team_ecju_query()
    CaseListPage(driver).click_apply_filters_button()


@when("I click advanced filters")
def i_show_advanced_filters(driver, context):
    CaseListPage(driver).click_clear_filters_button()


@then("I can see all advanced filters")
def i_can_see_all_advanced_filters(driver, context):
    CaseListPage(driver).assert_all_advanced_filters_available()


@when("I filter by case reference")
def i_filter_by_case_reference(driver, context):
    CaseListPage(driver).filter_by_exporter_application_reference(context.app_name)

