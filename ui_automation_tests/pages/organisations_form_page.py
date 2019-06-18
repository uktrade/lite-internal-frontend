class OrganisationsFormPage():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

    def click_new_organisation_btn(self):
        new_organisation_btn = self.driver.find_element_by_css_selector("a[href*='organisations/register']")
        new_organisation_btn.click()

    def enter_name(self, text):
        self.driver.find_element_by_id("name").send_keys(text)

    def enter_eori_number(self, text):
        self.driver.find_element_by_id("eori_number").send_keys(text)

    def enter_sic_number(self, text):
        self.driver.find_element_by_id("sic_number").send_keys(text)

    def enter_vat_number(self, text):
        self.driver.find_element_by_id("vat_number").send_keys(text)

    def enter_registration_number(self, text):
        self.driver.find_element_by_id("registration_number").send_keys(text)

    def click_submit(self):
        submit = self.driver.find_element_by_xpath("//*[@action='submit']")
        submit.click()

