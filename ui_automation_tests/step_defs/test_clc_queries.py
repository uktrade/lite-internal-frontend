from pytest_bdd import when, then, parsers, scenarios
from pages.clc_queries_pages import ClcQueriesPages
from pages.shared import Shared

scenarios('../features/clc_query.feature', strict_gherkin=False)

@when('I click Respond to query')
def respond_to_query(driver):
    clcquerypage = ClcQueriesPages(driver)
    clcquerypage.respond_to_query()

@when(parsers.parse('I respond "{controlled}", "{control_code}", "{report}", "{comment}" and click continue'))
def enter_response(driver, controlled, control_code, report, comment):
    clcquerypage = ClcQueriesPages(driver)
    clcquerypage.is_good_controlled(controlled)
    clcquerypage.control_code_response(control_code)
    clcquerypage.choose_report_summary(report)
    clcquerypage.enter_a_comment(controlled)
    shared = Shared(driver)
    shared.click_submit()


@when('I submit response')
def submit_response(driver):
    clcquerypage = ClcQueriesPages(driver)
    clcquerypage.click_submit()


@then('I see case is closed')
def check_case_closed(driver):
    clcquerypage = ClcQueriesPages(driver)
    assert clcquerypage.case_closed()
