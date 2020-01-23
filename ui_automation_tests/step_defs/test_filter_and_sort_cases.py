from pytest_bdd import given, when, then, parsers, scenarios

from pages.queues_pages import QueuesPages
from shared.tools.helpers import get_formatted_date_time_m_d_h_s
from shared.tools.utils import get_lite_client
from pages.shared import Shared

from shared.tools.wait import wait_until_page_is_loaded
from ui_automation_tests.pages.case_list_page import CaseListPage

scenarios("../features/filter_and_sort_cases.feature", strict_gherkin=False)


@given("a queue has been created")
def create_queue(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_queue.add_queue("queue" + get_formatted_date_time_m_d_h_s())
    context.queue_name = lite_client.context["queue_name"]


@when("case has been moved to new Queue")
def assign_case_to_queue(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    lite_client.seed_case.assign_case_to_queue()


@then(parsers.parse('"{number}" cases are shown'))
def num_cases_appear(driver, context, number):
    assert int(number) == Shared(driver).get_number_of_rows_in_lite_table(), "incorrect number of cases are shown"


@when(parsers.parse('filter status has been changed to "{status}"'))
def filter_status_change(driver, context, status):
    CaseListPage(driver).select_filter_status_from_dropdown(status)
    CaseListPage(driver).click_apply_filters_button()


@when("I click clear filters")
def i_show_filters(driver, context):
    CaseListPage(driver).click_clear_filters_button()


@when("I hide filters")
def i_hide_filters(driver, context):
    CaseListPage(driver).click_hide_filters_link()


@when("I sort cases by status")
def i_sort_cases_by(driver, context):
    wait_until_page_is_loaded(driver)
    CaseListPage(driver).sort_by_status()


@then(parsers.parse('the case at index "{index}" has the status of "{status}"'))
def the_cases_are_in_order_of(driver, index, status):
    assert status in Shared(driver).get_lite_row_text_by_index(index), status + " is not in the correct order"


@then("the filters are shown")
def the_filters_are_shown(driver, context):
    assert CaseListPage(driver).is_filters_visible(), "filters are not shown"


@then("the filters are hidden")
def the_filters_are_hidden(driver, context):
    driver.set_timeout_to(0)
    assert not CaseListPage(driver).is_filters_visible(), "filters are shown"
    driver.set_timeout_to_10_seconds()


@then("there are no cases shown")  # noqa
def no_cases_shown(driver):
    assert (
        "There are no cases to show with those filters" in QueuesPages(driver).get_no_cases_text()
    ), "There are cases shown in the newly created queue."


@when("I create a clc query")  # noqa
def create_clc_query(driver, apply_for_clc_query, context):
    pass
