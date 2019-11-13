from pytest_bdd import when, then, parsers, scenarios, given
from pages.clc_queries_pages import ClcQueriesPages
from pages.shared import Shared

scenarios("../features/clc_query.feature", strict_gherkin=False)


@when("I click Respond to query")
def respond_to_query(driver):
    ClcQueriesPages(driver).click_respond_to_query()


@when(
    parsers.parse(
        'I respond "{controlled}", "{control_list_entry}", "{report}", "{comment}" and click continue'
    )
)
def enter_response(driver, controlled, control_list_entry, report, comment):
    clc_query_page = ClcQueriesPages(driver)
    clc_query_page.click_is_good_controlled(controlled)
    clc_query_page.type_in_to_control_list_entry(control_list_entry)
    clc_query_page.choose_report_summary(report)
    clc_query_page.enter_a_comment(controlled)
    Shared(driver).click_submit()


@when("I submit response")
def submit_response(driver):
    Shared(driver).click_submit()


@then("I see case is closed")
def check_case_closed(driver):
    assert ClcQueriesPages(driver).is_clc_query_case_closed()


@then("I do not see the respond to query button")
def no_respond_to_query_button(driver):
    assert not ClcQueriesPages(driver).is_respond_to_query_button_present()


@then("I see the respond to query button")
def no_respond_to_query_button(driver):
    assert ClcQueriesPages(driver).is_respond_to_query_button_present()
