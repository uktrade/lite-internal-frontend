from pytest_bdd import when, then, scenarios, given, parsers

from fixtures.add_a_flag import get_flag_of_level
from pages.application_page import ApplicationPage
from pages.case_page import CasePage
import shared.tools.helpers as utils
from pages.shared import Shared

scenarios("../features/assign_case_flags_to_case.feature", strict_gherkin=False)


@when("I click edit flags on the first destination")
def click_edit_destination_flags_link(driver):
    case_page = CasePage(driver)
    case_page.select_destination(0)
    case_page.click_edit_destinations_flags()


@when("I click edit flags on the first good")
def click_edit_goods_flags_link(driver):
    case_page = CasePage(driver)
    case_page.select_first_good()
    case_page.click_edit_goods_flags()


@then("the previously created goods flag is assigned to the good")
def assert_flag_is_assigned(driver, context):
    assert CasePage(driver).is_goods_flag_applied(context.flag_name)


@when("I click the expand flags dropdown")  # noqa
def click_chevron(driver, context):
    ApplicationPage(driver).click_expand_flags(context.case_id)


@then("I see added flags to case")
def i_see_added_flags(context, driver):
    case_row = driver.find_element_by_id(context.case_id)
    if "(3 of " in case_row.text:
        ApplicationPage(driver).click_expand_flags(context.case_id)
    text = driver.find_element_by_id("flags-" + context.case_id).text
    for level in context.flags:
        assert context.flags[level]["name"] in text


@then(parsers.parse('the "{audit_type}" flag appears in the audit trail'))
def verify_organisation_flag_audit(driver, context, audit_type):
    body = Shared(driver).get_audit_trail_text()
    assert context.flags["Organisation"]["name"] in body
    assert audit_type in body


@then("I see added flags to case in case view")
def see_added_flags_to_case(driver, context):
    list_of_flags = driver.execute_script("return document.getElementById('case-flags').textContent")
    for level in context.flags:
        assert context.flags[level]["name"] in list_of_flags


@given("all types of flags exist")
def get_all_flags(api_test_client, context):
    levels = ["Case", "Good", "Organisation", "Destination"]
    flags = {}
    all_flags = api_test_client.flags.get_list_of_flags()
    for level in levels:
        flag = get_flag_of_level(all_flags, level)
        if not flag:
            flag = api_test_client.flags.add_flag(level + utils.get_formatted_date_time_m_d_h_s(), level)
        flags[level] = {"id": flag["id"], "name": flag["name"]}
    context.flags = flags
