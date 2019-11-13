import shared.tools.helpers as utils
from pages.clc_queries_pages import ClcQueriesPages
from pages.shared import Shared
from pytest_bdd import given, when, then, scenarios, parsers
from pages.assign_flags_to_case import CaseFlagsPages
from pages.flags_pages import FlagsPages
from pages.application_page import ApplicationPage
from pages.good_summary_page import GoodSummaryPage
from pages.shared import Shared

from pages.header_page import HeaderPage

scenarios("../features/review_goods.feature", strict_gherkin=False)


@when("I select goods and click review")
def click_edit_flags_link(driver):
    application_page = ApplicationPage(driver)
    application_page.select_a_good()
    application_page.click_review_goods()


@when("I click on add report summary")
def click_edit_flags_link(driver):
    good_summary_page = GoodSummaryPage(driver)
    good_summary_page.click_add_report_summary()


@when(
    parsers.parse(
        'I respond "{controlled}", "{control_list_entry}", "{report}", "{comment}" and click continue'
    )
)
def click_continue(driver, controlled, control_list_entry, report, comment, context):
    query_page = ClcQueriesPages(driver)
    query_page.click_is_good_controlled(controlled)
    query_page.type_in_to_control_list_entry(control_list_entry)
    context.goods_control_list_entry = control_list_entry
    query_page.choose_report_summary(report)
    query_page.enter_a_comment(comment)
    Shared(driver).click_submit()


@then("the control list is present on goods review page")
def check_control_list_code(driver, context):
    shared = Shared(driver)
    rows = shared.get_rows_in_lite_table()
    if len(rows) == 0:
        assert False, "Table rows not found"
    for row in rows:
        assert context.goods_control_list_entry in row.text


@then("I do not see the review goods button")
def no_respond_to_query_button(driver):
    assert not ApplicationPage(driver).is_review_goods_button_present()


@then("I see review goods button")
def no_respond_to_query_button(driver):
    assert ApplicationPage(driver).is_review_goods_button_present()
