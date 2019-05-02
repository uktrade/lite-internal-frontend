from selenium.webdriver.common.by import By
import helpers.helpers as utils
import pytest
import  logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url):
    driver.get(internal_url)
    # driver.maximize_window()
    log.info(driver.current_url)


def test_new_organisation_setup(driver, open_internal_hub):
    log.info("Setting up new organisation")

    manage_organisations_btn = driver.find_element_by_css_selector("a[href*='/organisations']")
    manage_organisations_btn.click()

    exists = utils.is_element_present(driver, By.XPATH ,"//*[text()[contains(.,'Test Org')]]")
    if not exists:
        # New Organisation
        new_organisation_btn = driver.find_element_by_css_selector("a[href*='/register']")
        new_organisation_btn.click()

        driver.find_element_by_id("name").send_keys("Test Org")
        driver.find_element_by_id("eori_number").send_keys("GB987654312000")
        driver.find_element_by_id("sic_number").send_keys("73200")
        driver.find_element_by_id("vat_number").send_keys("123456789")
        driver.find_element_by_id("registration_number").send_keys("000000011")
        driver.find_element_by_id("address").send_keys("123 Cobalt Street")
        # driver.find_element_by_id("admin_user_first_name").send_keys("Test")
        # driver.find_element_by_id("admin_user_last_name").send_keys("User1")
        driver.find_element_by_id("admin_user_email").send_keys("test@mail.com")

        submit = driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
        assert exists


def test_teardown(driver):
    driver.quit()

