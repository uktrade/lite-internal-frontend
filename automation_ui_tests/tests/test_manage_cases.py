import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from automation_ui_tests.pages.department_of_international_trade_hub_page import DepartmentOfInternationalTradeHub
from automation_ui_tests.pages.exporter_hub import ExporterHub

import datetime


class ManageCasesTest(unittest.TestCase):
    @classmethod
    def setUp(cls):

        project_root = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(project_root)
        print("dir:" + base_dir)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.implicitly_wait(10)

        dit_hub_page = DepartmentOfInternationalTradeHub(cls)
        cls.driver.get(dit_hub_page.url)

    def test_view_submitted_cases_in_work_queue(self):
        driver = self.driver
        exporterHub = ExporterHub(driver)
        dit_hub_page = DepartmentOfInternationalTradeHub(driver)

        print("Test Started")

        # Submit application
        print("submitting application on Exporter Hub")
        exporterHub.go_to()
        self.driver.find_element_by_css_selector("a[href*='/new-application/']").click()
        self.driver.find_element_by_css_selector("a[href*='/start']").click()
        appTimeId = str(datetime.datetime.now())
        self.driver.find_element_by_id("name").send_keys("Test App" + appTimeId)
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("control_code").send_keys("code123")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("destination").send_keys("Mexico")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("usage").send_keys("shooting usage")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_id("activity").send_keys("test activity")
        exporterHub.click_save_and_continue()
        self.driver.find_element_by_css_selector("button[type*='submit']").click()
        print("Application submitted")

        # navigate to DIT Hub page
        dit_hub_page.go_to()
        print("Navigated to Department Of International Trade Hub")

        dit_hub_page.click_manage_cases_btn()
        print("Clicked onto Manage Cases")

        # Verify Case is in the New Cases Work Queue
        print("Verifying Case is in the New Cases Work Queue")
        cases_table = self.driver.find_element_by_class_name("lite-table")
        self.assertTrue(self.is_element_present(By.XPATH,"//*[text()[contains(.,'" + appTimeId + "')]]"))
        print("Application found in work queue")

        print("Test Complete")



    @classmethod
    def tearDown(inst):
        # close the browser window
        inst.driver.quit()

    def is_element_present(self, how, what):
        """
        Helper method to confirm the presence of an element on page
        :params how: By locator type
        :params what: locator value
        """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

if __name__ == '__main__':
    unittest.main(verbosity=2)