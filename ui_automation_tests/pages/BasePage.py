from selenium.webdriver.remote.webdriver import WebDriver

from ui_automation_tests.shared import functions
from ui_automation_tests.shared.tools.wait import wait_until_page_is_loaded


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        # Wait for the cases list to load before interacting with the page
        if functions.element_with_id_exists(self.driver, "link-queue"):
            wait_until_page_is_loaded(driver)

        # The case header is sticky and can often overlay elements preventing clicks,
        # therefore disable the stickyness of the header when running tests
        if functions.element_with_id_exists(self.driver, "app-header"):
            self.driver.execute_script("document.getElementById('app-header').style.position = 'relative';")
