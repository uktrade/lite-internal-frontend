import datetime
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.application_page import ApplicationPage
from pages.exporter_hub import ExporterHub
from conftest import context
import helpers.helpers as utils

scenarios('../features/manage_cases.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I click progress application')
def click_post_note(driver):
    application_page = ApplicationPage(driver)
    application_page.click_progress_application()


@when(parsers.parse('I select status "{status}" and save'))
def select_status_save(driver, status):
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]").click()


@then('the status has been changed in the header')
def status_has_been_changed_in_header(driver):
    application_page = ApplicationPage(driver)
    for header in application_page.get_text_of_headers():
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == context.status


#TODO dependency
@when('I click applications')
def i_click_applications(driver):
    exporter = ExporterHub(driver)
    exporter.click_applications()


@then('the status has been changed in exporter')
def i_click_applications(driver):
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_time_id + "')]]/following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == context.status
