import re
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from conftest import context
from pages.application_page import ApplicationPage
from pages.record_decision_page import RecordDecision
from pages.exporter_hub import ExporterHub
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


@when('I click record decision')
def click_post_note(driver):
    application_page = ApplicationPage(driver)
    application_page.click_record_decision()


@when(parsers.parse('I "{grant_or_deny}" application'))
def grant_or_deny_decision(driver, grant_or_deny):
    record = RecordDecision(driver)
    if grant_or_deny == "grant":
        record.click_on_grant_licence()
    elif grant_or_deny == "deny":
        record.click_on_deny_licence()


@when(parsers.parse('I select decision "{number}" with optional text "{optional_text}"'))
def select_decision(driver, number, optional_text):
    record = RecordDecision(driver)
    record.click_on_decision_number(number)
    context.decision_number = number
    record.enter_optional_text(optional_text)
    context.optional_text = optional_text


@then(parsers.parse('I see application "{grant_or_deny}"'))
def see_application_granted_or_denied(driver, grant_or_deny):
    record = RecordDecision(driver)
    details = driver.find_elements_by_css_selector(".lite-heading-s")
    for header in details:
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            if grant_or_deny == "granted":
                assert status_detail == "Approved"
            elif grant_or_deny == "denied":
                assert status_detail == "Under final review"
                assert record.get_text_of_denial_reasons_headers(0) == "This case was denied because"
                assert record.get_text_of_denial_reasons_headers(1) == "Further information"
                #todo ask dev to put a selector in here
                assert record.get_text_of_denial_reasons_listed(5) == context.decision_number
                assert record.get_text_of_denial_reasons_listed(6) == context.optional_text


@when('dates are in chronological order')
def select_status_save(driver):
    application_page = ApplicationPage(driver)


@when(parsers.parse('I select status "{status}" and save'))
def select_status_save(driver, status):
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]").click()


@then('the status has been changed in the application')
def status_has_been_changed_in_header(driver):
    application_page = ApplicationPage(driver)
    for header in application_page.get_text_of_application_headings():
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == context.status
    # this also tests that the activities are in reverse chronological order as it is expecting the status change to be first.
    assert context.status.lower() in application_page.get_text_of_case_note_subject(0)
    x = re.search("^[0-9]{2}):([0-9]{2})(am|pm) ([0-9][0-9]) (January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]{4,})$", application_page.get_text_of_activity_dates(0))

    assert x

#TODO exporter dependency
@when('I click applications')
def i_click_applications(driver):
    exporter = ExporterHub(driver)
    exporter.click_applications()


@then('the status has been changed in exporter')
def i_click_applications(driver):
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_time_id + "')]]/following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == context.status


@then('the application headers and information are correct')
def application_headers_and_info_are_correct(driver):
    assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[0].text == "APPLICANT"
    assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[1].text == "ACTIVITY"
    assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[2].text == "LAST UPDATED"
    assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[3].text == "STATUS"
    assert driver.find_elements_by_css_selector(".lite-information-board .lite-heading-s")[4].text == "USAGE"
    #  this is hard coded from the organisation that is created as part of setup
    assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[0].text == "Unicorns Ltd"
    assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[1].text == "Trading" or driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[1].text == "Brokering"
    #TODO commented out below line due to bug LT-1281
    #assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[2].text == context.date_time_of_update
    assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[3].text == context.status
    assert driver.find_elements_by_css_selector(".lite-information-board .govuk-label")[4].text == "None"

