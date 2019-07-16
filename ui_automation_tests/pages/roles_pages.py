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
        self.driver.find_element_by_id(value).click()

    def click_add_a_role_button(self):
        self.driver.find_element_by_id("button_add_role").click()

    def edit_default_role_to_have_permission(self, permission):
        if not self.driver.find_element_by_id(permission).is_selected():
            self.select_permissions(permission)

    def remove_all_permissions_from_default_role(self):
        elements = self.driver.find_elements_by_css_selector(".govuk-checkboxes__input")
        for element in elements:
            if element.is_selected():
                element.click()
