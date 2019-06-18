import unittest
import datetime
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.exporter_hub import ExporterHub
from pages.manage_cases_page import ManageCasesPage
import helpers.helpers as utils
import logging
import time
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)



def test_record_decision(driver, open_internal_hub, exporter_url, internal_url):
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)

    exporter_hub.go_to(exporter_url)
    if "login" in driver.current_url:
        log.info("logging in as test@mail.com")
        exporter_hub.login("test@mail.com", "password")

    # Submit application
    log.info("submitting application on Exporter Hub")
    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Department Of International Trade Hub")

    # check details page
    log.info("Clicking into application...")
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    # Record Decision
    record_decision_btn = driver.find_element_by_xpath("//*[text()[contains(.,'Record Decision')]]")
    record_decision_btn.click()

    # Grant Licence
    grant_licence_radio = driver.find_element_by_css_selector("label[for='radio-grant']")
    grant_licence_radio.click()
    log.info("granting Licence")

    save_btn = driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]")
    save_btn.click()

    log.info("Verifying status changed to approved")
    details = driver.find_elements_by_css_selector(".lite-heading-s")
    for header in details:
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == "Approved"

    dit_hub_page.go_to(internal_url)

    # Check application status is changed
    status = driver.find_element_by_xpath(
        "//*[text()[contains(.,'" + app_id + "')]]/../following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Approved"

    # Deny Licence
    logging.info("Denying Licence")
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    record_decision_btn = driver.find_element_by_xpath("//*[text()[contains(.,'Record Decision')]]")
    record_decision_btn.click()

    deny_licence_radio = driver.find_element_by_css_selector("label[for='radio-deny']")
    deny_licence_radio.click()

    save_btn = driver.find_element_by_xpath("//button[text()[contains(.,'Save')]]")
    save_btn.click()

    logging.info("Verifying status changed to Declined")
    details = driver.find_elements_by_css_selector(".lite-heading-s")
    for header in details:
        if header.text == "STATUS":
            status_detail = header.find_element_by_xpath("./following-sibling::p").text
            assert status_detail == "Declined"

    dit_hub_page.go_to(internal_url)

    # Check application status is changed
    status = driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]/../following-sibling::td[last()]")
    assert status.is_displayed()
    assert status.text == "Declined"
    print("Test Complete")


def test_teardown(driver):
    driver.quit()
