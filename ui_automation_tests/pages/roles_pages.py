from selenium.webdriver.support.select import Select


class RolesPages():

    def __init__(self, driver):
        self.driver = driver
        self.add_role_text_field = "name"
        self.add_role_button = ".govuk-button[href*='roles/add']"

    def enter_role_name(self, text):
        self.driver.find_element_by_id(self.add_role_text_field).clear()
        self.driver.find_element_by_id(self.add_role_text_field).send_keys(text)

    def select_permissions(self, value):
        select = Select(self.driver.find_element_by_id('permissions'))
        select.select_by_visible_text(value)

    def click_add_a_role_button(self):
        self.driver.find_element_by_css_selector(self.add_role_button).click()