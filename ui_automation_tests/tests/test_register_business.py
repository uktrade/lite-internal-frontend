import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pages.dit_hub_page import DepartmentOfInternationalTradeHub
from pages.register_a_business_page import RegisterABusinessPage
from pages.organisations_page import OrganisationsPage
import helpers.helpers as utils
import datetime
import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_register_a_business(driver, open_internal_hub, internal_url):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    time_id = datetime.datetime.now().strftime("%m%d%H%M%S")
    register_page.enter_business_name("Test Business " + time_id)
    register_page.enter_eori_number("GB987654312000")
    register_page.enter_sic_number("73200")
    register_page.enter_vat_number("123456789")
    register_page.enter_company_registration_number("000000011")
    register_page.enter_address("123 Cobalt Street")
    register_page.enter_admin_user_email("joe@bloss.com")

    logging.info("Submitting...")
    register_page.click_submit()

    registration_complete_message = driver.find_element_by_tag_name("h1").text
    assert registration_complete_message == "Registration Complete"
    logging.info("Application Submitted")

    # verify application is in organisations list
    dit_hub_page.go_to(internal_url)
    dit_hub_page.click_manage_organisations_link()

    assert utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + time_id + "')]]")
    logging.info("Test Complete")


def test_cancel_register_a_business(driver, open_internal_hub):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    logging.info("Cancelling...")
    register_page.click_cancel()

    title = driver.title
    assert "Organisations" in title

    logging.info("Application Cancelled")
    logging.info("Test Complete")


def test_cannot_submit_without_required_fields(driver, open_internal_hub):
    dit_hub_page = DepartmentOfInternationalTradeHub(driver)
    register_page = RegisterABusinessPage(driver)
    organisations_page = OrganisationsPage(driver)

    dit_hub_page.click_manage_organisations_link()

    # New Organisation
    logging.info("Registering a new business")
    organisations_page.click_new_organisation_btn()

    logging.info("clicked submit")
    register_page.click_submit()

    driver.find_element_by_id("error-summary-title").is_displayed()

    title = driver.title
    assert "Overview" not in title

    logging.info("Test Complete")


def test_teardown(driver):
    driver.quit()
