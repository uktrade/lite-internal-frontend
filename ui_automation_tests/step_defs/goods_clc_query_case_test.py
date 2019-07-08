from pytest_bdd import scenarios, given, when, then, parsers
from pages.goods_list import GoodsList
from pages.exporter_hub_page import ExporterHubPage
from pages.add_goods_page import AddGoodPage, CaseListPage
from conftest import context
import helpers.helpers as utils

scenarios('../features/add_goods.feature', strict_gherkin=False)


@when('I click add a good button')
def click_add_from_organisation_button(driver):
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()


@when(parsers.parse('I add a good a clc-case good with description "{description}"'))
def add_new_good(driver, description, controlled, controlcode, incorporated, part):
    exporter_hub = ExporterHubPage(driver)
    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % (description, date_time)
    context.good_description = good_description
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_control_unsure_confirmation(description)
    add_goods_page.enter_control_unsure_details("%s unsure" % description)
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product()
    exporter_hub.click_save_and_continue()
    add_goods_page.select_control_unsure_confirmation()
    exporter_hub.click_save_and_continue()


@when('I see clc-good in goods list')
def assert_good_is_in_list(driver):
    goods_list = AddGoodPage(driver)
    case_id = goods_list.assert_good_is_displayed_and_return_case_id(context.good_description)
    context.case_id = case_id


@then('I see the clc-case previously created')
def assert_case_is_present(driver):
    case_list_page = CaseListPage(driver)
    case_list_page.assert_case_is_present(context.case_id)
