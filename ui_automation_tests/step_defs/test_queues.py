from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from selenium.webdriver.support.ui import Select
import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.queues_pages import QueuesPages
from pages.shared import Shared
from pages.case_list_page import CaseListPage

scenarios('../features/queues.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I go to queues')
def go_to_queues(driver):
    HeaderPage(driver).click_lite_menu()
    HeaderPage(driver).click_queues()


@when('I click on add a queue')
def click_on_add_queue(driver):
    QueuesPages(driver).click_add_a_queue_button()


@when('I edit the new queue')
def click_on_edit_queue(driver, context):
    driver.find_element_by_xpath("//*[text()[contains(.,'" + context.queue_name + "')]]/following-sibling::td[last()]/a").click()
    context.queue_name = str(context.queue_name)[:12] + "edited"
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()


@when(parsers.parse('I enter in queue name "{queue_name}"'))
def add_a_queue(driver, queue_name, context):
    if queue_name == " ":
        context.queue_name = queue_name
    else:
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string))-14:]
        context.queue_name = queue_name + extra_string
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()


@then('I see the new queue')
def see_queue_in_queue_list(driver, context):
    assert context.queue_name in Shared(driver).get_text_of_body()


@then('I see previously created application')
def see_queue_in_queue_list(driver, context):
    assert driver.find_element_by_css_selector('.lite-cases-table').find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").is_displayed()


@then('I dont see previously created application')
def dont_see_queue_in_queue_list(driver, context):
    assert 'There are no new cases to show.' in driver.find_element_by_css_selector('.govuk-caption-l').text


@then('I dont see the clc-case previously created')
def i_dont_see_the_clc_query_in_the_list(driver, context):
    assert 'There are no new cases to show.' in driver.find_element_by_css_selector('.govuk-caption-l').text


@when('I add case to new queue')
def move_case_to_new_queue(driver, context):
    driver.find_element_by_css_selector('.govuk-button[href*="move"]').click()
    driver.find_element_by_id(context.queue_name).click()
    Shared(driver).click_submit()


@when('I deselect all queues')
def deselect_all_queues(driver, context):
    driver.find_element_by_css_selector('.govuk-button[href*="move"]').click()
    elements = driver.find_elements_by_css_selector('#checkbox-list .govuk-body')
    for element in elements:
        driver.find_element_by_id(element.text).click()
    Shared(driver).click_submit()


@when('I move case to new cases original queue and remove from new queue')
def move_case_to_original_queue(driver, context):
    driver.find_element_by_css_selector('.govuk-button[href*="move"]').click()
    driver.find_element_by_id(context.queue_name).click()
    driver.find_element_by_id("New Cases").click()
    Shared(driver).click_submit()


@when('I click on new queue in dropdown')
def new_queue_shown_in_dropdown(driver, context):
    driver.find_element_by_id('queue-title').click()
    elements = driver.find_elements_by_css_selector('.lite-dropdown .lite-dropdown--item')
    for idx, element in enumerate(elements):
        if element.text == context.queue_name:
            driver.execute_script("document.getElementsByClassName('lite-dropdown--item')[" + str(idx) + "].scrollIntoView(true);")
            element.click()
            break


@then('I click on the clc-case previously created')
@when('I click on the clc-case previously created')
def assert_case_is_present(driver, register_organisation, apply_for_clc_query, context):
    case_list_page = CaseListPage(driver)
    assert case_list_page.assert_case_is_present(context.case_id)
    driver.find_element_by_css_selector('.lite-cases-table').find_element_by_xpath("//*[text()[contains(.,'" + context.case_id + "')]]").click()
