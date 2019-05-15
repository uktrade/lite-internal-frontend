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


@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_add_case_notes(driver, internal_url, exporter_url):
    log.info("Test Started")
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    case_view_page = ManageCasesPage(driver)

    # Submit application
    log.info("submitting application on Exporter Hub")
    exporter_hub.go_to(exporter_url)
    exporter_hub.login("test@mail.com", "password")

    time_id = datetime.datetime.now().strftime("%m%d%H%M")

    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Internal Hub")
    # Open Case is in the New Cases Work Queue
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    case_view_page.enter_case_note("First case note")
    case_view_page.click_post_note_btn()

    case_notes = driver.find_elements_by_css_selector(".lite-case-notes > .lite-case-note--new")
    for note in case_notes:
        assert "First case note" in note.text

    print("Test Complete")


def test_case_notes_empty_note_space_char_max(driver, internal_url, exporter_url):
    log.info("Test Started")
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    case_view_page = ManageCasesPage(driver)

    # Submit application
    log.info("submitting application on Exporter Hub")
    exporter_hub.go_to(exporter_url)
    exporter_hub.login("test@mail.com", "password")

    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Internal Hub")
    # Open Case is in the New Cases Work Queue
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    max_characters = utils.repeat_to_length(" ", 2200)
    case_view_page.enter_case_note(max_characters)

    post_disabled = driver.find_element_by_id("button-post-note").get_attribute("disabled") == "true"
    assert post_disabled, "should not be able to post an empty case note with space characters"


def test_case_notes_too_many_chars(driver, internal_url, exporter_url):
    log.info("Test Started")
    exporter_hub = ExporterHub(driver)
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    case_view_page = ManageCasesPage(driver)

    # Submit application
    log.info("submitting application on Exporter Hub")
    exporter_hub.go_to(exporter_url)
    exporter_hub.login("test@mail.com", "password")

    time_id = datetime.datetime.now().strftime("%m%d%H%M")
    app_name = "Test Application " + time_id
    exporter_hub.create_application(name=str(app_name), destination="Cuba", usage="Test usage", activity="Testing")
    app_id = driver.current_url[-36:]
    log.info("Application submitted")

    # navigate to DIT Hub page
    dit_hub_page.go_to(internal_url)
    log.info("Navigated to Internal Hub")
    # Open Case is in the New Cases Work Queue
    driver.find_element_by_xpath("//*[text()[contains(.,'" + app_id + "')]]").click()

    max_characters = utils.repeat_to_length("T", 2200)
    case_view_page.enter_case_note(max_characters)

    case_note_warning = case_view_page.get_case_note_warning()

    assert case_note_warning == "You have 0 characters remaining"

    case_view_page.enter_case_note("T")

    case_note_warning = case_view_page.get_case_note_warning()
    assert case_note_warning == "You have 1 character too many"

    post_disabled = driver.find_element_by_id("button-post-note").get_attribute("disabled") == "true"
    assert post_disabled

    print("Test Complete")


def test_teardown(driver):
    driver.quit()
