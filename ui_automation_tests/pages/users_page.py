from selenium.webdriver.support.ui import Select

from pages.shared import Shared
from shared import functions, selectors
from ui_automation_tests.shared.BasePage import BasePage


class UsersPage(BasePage):
    BUTTON_ADD_USER_ID = "button-add-user"
    MANAGE_ROLES_BUTTON = "button-manage-roles"
    EMAIL = "email"
    TEAM = "team"
    ROLE = "role"
    QUEUE = "default_queue"
    LINK_CHANGE_EMAIL_ID = "link-edit-email"
    BUTTON_DEACTIVATE_USER_ID = "button-deactivate-user"
    BUTTON_REACTIVATE_USER_ID = "button-reactivate-user"
    DEACTIVATE_ARE_YOU_SURE_BUTTON_ID = "deactivated_button"
    REACTIVATE_ARE_YOU_SURE_BUTTON_ID = "reactivated_button"
    INPUT_EMAIL_FILTER_ID = "email"


    def click_add_a_user_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_USER_ID).click()

    def enter_email(self, email):
        self.driver.find_element_by_id(self.EMAIL).clear()
        self.driver.find_element_by_id(self.EMAIL).send_keys(email)

    def select_option_from_team_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.TEAM))
        select.select_by_visible_text(value)

    def select_option_from_role_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.ROLE))
        select.select_by_visible_text(value)

    def select_option_from_default_queue_drop_down_by_visible_text(self, value):
        select = Select(self.driver.find_element_by_id(self.QUEUE))
        select.select_by_visible_text(value)

    def select_option_from_team_drop_down_by_value(self):
        select = Select(self.driver.find_element_by_id(self.TEAM))
        select.select_by_index(2)

    def click_on_manage_roles(self):
        self.driver.find_element_by_id(self.MANAGE_ROLES_BUTTON).click()

    def click_change_email_link(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_EMAIL_ID).click()

    def click_deactivate_user(self):
        self.driver.find_element_by_id(self.BUTTON_DEACTIVATE_USER_ID).click()
        self.driver.find_element_by_id(self.DEACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def click_reactivate_user(self):
        self.driver.find_element_by_id(self.BUTTON_REACTIVATE_USER_ID).click()
        self.driver.find_element_by_id(self.REACTIVATE_ARE_YOU_SURE_BUTTON_ID).click()

    def go_to_user_page(self, context):
        Shared(self.driver).filter_by_name(context.added_email)
        element_id = "link-" + context.added_email
        self.driver.find_element_by_id(element_id).click()

    def filter_by_name(self, name):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_EMAIL_FILTER_ID).clear()
        self.driver.find_element_by_id(self.INPUT_EMAIL_FILTER_ID).send_keys(name)
        self.driver.find_element_by_css_selector(selectors.BUTTON_APPLY_FILTERS).click()
