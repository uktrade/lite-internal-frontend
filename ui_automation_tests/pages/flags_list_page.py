from shared import functions
from shared.BasePage import BasePage


class FlagsListPage(BasePage):
    BUTTON_ADD_FLAG_ID = "button-add-a-flag"
    CHECKBOX_ONLY_SHOW_DEACTIVATED_NAME = "status"

    def click_add_a_flag_button(self):
        self.driver.find_element_by_id(self.BUTTON_ADD_FLAG_ID).click()

    def click_edit_link(self):
        self.driver.find_element_by_partial_link_text("Edit").click()

    def click_only_show_deactivated(self):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_name(self.CHECKBOX_ONLY_SHOW_DEACTIVATED_NAME).click()
        functions.click_apply_filters(self.driver)

    def click_deactivate_link(self):
        self.driver.find_element_by_partial_link_text("Deactivate").click()

    def click_reactivate_link(self):
        self.driver.find_element_by_partial_link_text("Reactivate").click()
