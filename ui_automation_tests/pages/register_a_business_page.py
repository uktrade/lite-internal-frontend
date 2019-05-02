from selenium.webdriver.support.ui import Select


class RegisterABusinessPage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.queue_drop_down = "a[href*='/new-application/']"
        self.go_to_queue_btn = "button.govuk-button"

    def select_from_queue_drop_down(self, value):
        select = Select(self.find_element_by_name('queue'))
        select.select_by_visible_text(value)

    def click_go_to_queue_button(self):
        self.driver.find_element_by_css_selector(self.go_to_queue_btn).click()

    def enter_business_name(self, business_name):
        self.driver.find_element_by_id("name").clear()
        self.driver.find_element_by_id("name").send_keys(business_name)

    def enter_eori_number(self, eori_number):
        self.driver.find_element_by_id("eori_number").clear()
        self.driver.find_element_by_id("eori_number").send_keys(eori_number)

    def enter_sic_number(self, sic_number):
        self.driver.find_element_by_id("sic_number").clear()
        self.driver.find_element_by_id("sic_number").send_keys(sic_number)

    def enter_vat_number(self,vat_number):
        self.driver.find_element_by_id("vat_number").clear()
        self.driver.find_element_by_id("vat_number").send_keys(vat_number)

    def enter_company_registration_number(self, registration_number):
        self.driver.find_element_by_id("registration_number").clear()
        self.driver.find_element_by_id("registration_number").send_keys(registration_number)

    def enter_address(self, address):
        self.driver.find_element_by_id("address").clear()
        self.driver.find_element_by_id("address").send_keys(address)

    def enter_admin_user_email(self, email):
        self.driver.find_element_by_id("admin_user_email").click()
        self.driver.find_element_by_id("admin_user_email").send_keys(email)

    def click_submit(self):
        submit = self.driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

    def click_cancel(self):
        cancel_btn = self.driver.find_element_by_css_selector("a[href*='/organisations']")
        cancel_btn.click()
