from pytest_bdd import when, then, scenarios, parsers
import shared.tools.helpers as utils
from pages.shared import Shared

from ui_automation_tests.pages.flagging_rules_pages import FlaggingRulePages
from ui_automation_tests.pages.routing_rules_pages import RoutingRulesPage

scenarios("../features/routing_rules.feature", strict_gherkin=False)


@when("I go to routing rules list")
def go_to_routing_rules(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/routing-rules/")


@then("I see the routing rule in the rule list")
def see_flag_in_list(driver, context):
    assert utils.find_paginated_item_by_id(context.queue_id, driver)


@when(
    parsers.parse(
        'I add a routing rule of tier "{tier}", a status of "{case_status}", my queue, and all additional rules'
    )
)
def create_routing_rule(driver, context, tier, case_status):
    routing_rules_page = RoutingRulesPage(driver)
    routing_rules_page.create_new_routing_rule()
    routing_rules_page.initial_details_form(
        tier=tier, case_status=case_status, queue=context.queue_name, additional_rules=True
    )
    Shared(driver).click_submit()

    routing_rules_page.select_case_type_by_text("Standard Individual Export Licence")
    Shared(driver).click_submit()

    routing_rules_page.select_flag(context.flag_name)
    Shared(driver).click_submit()

    routing_rules_page.enter_country("China")
    Shared(driver).click_submit()

    routing_rules_page.select_first_user()
    Shared(driver).click_submit()


@when(parsers.parse('I edit my routing rule with tier "{tier}", a status of "{case_status}", and no additional rules'))
def edit_flagging_rule(driver, context, tier, case_status):
    # select edit for my flagging rule
    utils.find_paginated_item_by_id(context.queue_id, driver).find_element_by_xpath("..").find_element_by_link_text(
        "Edit"
    ).click()

    routing_rules_page = RoutingRulesPage(driver)
    routing_rules_page.initial_details_form(
        tier=tier, case_status=case_status, queue=context.queue_name, additional_rules=False
    )
    Shared(driver).click_submit()


@then(parsers.parse('I see the routing rule in the list as "{status}" and tier "{tier}"'))
def routing_rule_status(driver, context, status, tier):
    text = utils.find_paginated_item_by_id(context.queue_id, driver).find_element_by_xpath("..").text
    assert status in text
    assert tier in text


@when("I deactivate my routing rule")
def deactivate_rule(driver, context):
    row = utils.find_paginated_item_by_id(context.queue_id, driver).find_element_by_xpath("..")
    RoutingRulesPage(driver).click_on_deactivate_rule(row)
    RoutingRulesPage(driver).click_confirm_deactivate_activate()
    Shared(driver).click_submit()
