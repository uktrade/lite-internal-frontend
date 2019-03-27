import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By



class register_business(unittest.TestCase):
    @classmethod
    def setUp(inst):
        # get the path of ChromeDriverServer
        dir = os.path.dirname(os.path.abspath(__file__))
        print("check"+dir)
        chrome_driver_path = dir + "/chromedriver"
        # create a new Chrome session
        inst.driver = webdriver.Chrome(chrome_driver_path)
        inst.driver.implicitly_wait(30)
        inst.driver.maximize_window()

        # navigate to the application home page
        inst.driver.get("http://localhost:7000/")

    def test_register_a_business(self):
        driver = self.driver

        register_a_businessBtn = driver.find_element_by_css_selector("a[href*='/register']")
        register_a_businessBtn.click()

        business_name_input = driver.find_element_by_id("name")
        eori_number_input = driver.find_element_by_id("eori_number")
        sic_number_input = driver.find_element_by_id("sic_number")
        vat_number_input = driver.find_element_by_id("vat_number")
        company_registration_number = driver.find_element_by_id("registration_number")
        address_input = driver.find_element_by_id("address")
        admin_user_email_input = driver.find_element_by_id("admin_user_email")

        business_name_input.send_keys("Test Business")
        eori_number_input.send_keys("GB987654312000")
        sic_number_input.send_keys("73200")
        vat_number_input.send_keys("123456789")
        company_registration_number.send_keys("000000011")
        address_input.send_keys("123 Cobalt Street")
        admin_user_email_input.send_keys("joe@bloss.com")

        submit = driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

        registration_complete_message = driver.find_element_by_tag_name("h1").text
        business_id = driver.find_element_by_css_selector(".govuk-panel--confirmation div").text[-36:]
        assert "Registration complete" == registration_complete_message

        driver.get("http://localhost:7000/")

        # verify application is in organisations list
        show_registered_organisations = driver.find_element_by_css_selector("a[href*='/show_orgs']")
        show_registered_organisations.click()

        self.assertTrue(self.is_element_present(By.XPATH,".//td/a[contains(@href,'" + business_id + "')]"))

    def test_cancel_register_a_business(self):
        driver = self.driver

        register_a_businessBtn = driver.find_element_by_css_selector("a[href*='/register']")
        register_a_businessBtn.click()

        cancel_btn = driver.find_element_by_css_selector("a[href*='/show_orgs']")
        cancel_btn.click()

        assert "Organisations" in driver.title

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