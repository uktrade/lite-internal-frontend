from pytest_bdd import when, then, scenarios, parsers
import shared.tools.helpers as utils
from pages.shared import Shared

from pages.flags_pages import FlagsPages

from ui_automation_tests.pages.flagging_rules_pages import FlaggingRulePages

scenarios("../features/flagging_rules.feature", strict_gherkin=False)


@when("I add a flag at level Case")  # noqa
def add_a_case_flag(driver, add_case_flag):  # noqa
    pass


@when("I add a flag at level Good")  # noqa
def add_a_flag(driver, add_good_flag):  # noqa
    pass


@when("I add a flag at level Destination")  # noqa
def add_a_flag(driver, add_destination_flag):  # noqa
    pass


@when("I go to flagging rules list")
def go_to_teams(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/flags/rules/")


@then("I see the flagging rule in the flag list")
def see_flag_in_list(driver, context):
    assert utils.find_paginated_item_by_id(context.flag_id, driver)


@when("I edit my flagging rule")
def edit_existing_flag(driver, context):
    elements = Shared(driver).get_links_in_cells_in_table()
    element_number = utils.get_element_index_by_text(elements, context.flag_name)
    elements[element_number + 2].click()
    flags_pages = FlagsPages(driver)
    context.flag_name = str(context.flag_name)[:18] + " 1"
    flags_pages.enter_flag_name(context.flag_name)
    Shared(driver).click_submit()


@when("I count the number of active flagging rules")
def count_active_flags(driver, context):
    context.original_number_of_active_flags = FlagsPages(driver).get_size_of_active_flags()
    context.original_number_of_deactivated_flags = FlagsPages(driver).get_size_of_inactive_flags()


@when("I deactivate the first active flagging rule")
def deactivate_first_active_flag(driver):
    FlaggingRulePages(driver).click_on_deactivate_flag()
    Shared(driver).click_submit()


@when("I click include deactivated")
def click_include_deactivated(driver):
    FlaggingRulePages(driver).click_include_deactivated()
    FlaggingRulePages(driver).click_apply_filters_button()


@then("I see one less active flagging rule")
def i_see_one_less_active_flag(driver, context):
    flags = FlagsPages(driver)
    number_of_active_flags = flags.get_size_of_active_flags()
    number_of_deactivated_flags = flags.get_size_of_inactive_flags()

    assert context.original_number_of_active_flags - number_of_active_flags == 1, "There is not one less flag"
    assert (
        context.original_number_of_deactivated_flags - number_of_deactivated_flags == -1
    ), "There is not one less deactivated flag"


@when("I reactivate the first deactivated flagging rule")
def reactivate_first_deactivated_flag(driver):
    FlaggingRulePages(driver).click_on_reactivate_flag()
    Shared(driver).click_submit()


@then("I see the original number of active flagging rule")
def i_see_the_original_number_of_active_flags(driver, context):
    flags = FlagsPages(driver)
    number_of_active_flags = flags.get_size_of_active_flags()
    number_of_deactivated_flags = flags.get_size_of_inactive_flags()

    assert (
        context.original_number_of_active_flags == number_of_active_flags
    ), "There is not equal an amount active flagging rules to before"
    assert (
        context.original_number_of_deactivated_flags == number_of_deactivated_flags
    ), "There is not equal an amount deactivated flags to before"


@when(parsers.parse('I add a flagging rule of type "{type}", with condition "{condition}", and flag'))
def create_flagging_rule(driver, context, type, condition):
    flagging_rules_page = FlaggingRulePages(driver)
    flagging_rules_page.create_new_flagging_rule()

    flagging_rules_page.select_flagging_rule_type(type)

    Shared(driver).click_submit()

    if type == "Case":
        flagging_rules_page.select_case_type(condition)
    elif type == "Destination":
        flagging_rules_page.select_country(condition)
    elif type == "Good":
        flagging_rules_page.enter_control_list(condition)

    flagging_rules_page.select_flag(context.flag_name)

    Shared(driver).click_submit()


@when(parsers.parse('I edit my "{type}" flagging rule with condition "{condition}"'))
def create_flagging_rule(driver, context, condition):
    flagging_rules_page = FlaggingRulePages(driver)

    # select edit for my flagging rule
    utils.find_paginated_item_by_id(context.flag_id, driver).find_element_by_xpath("..").find_element_by_link_text(
        "Edit"
    ).click()

    if type == "Case":
        flagging_rules_page.select_case_type(condition)
    elif type == "Destination":
        flagging_rules_page.select_country(condition)
    elif type == "Good":
        flagging_rules_page.enter_control_list(condition)

    Shared(driver).click_submit()
