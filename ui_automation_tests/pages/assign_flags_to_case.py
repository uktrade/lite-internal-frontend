from shared.BasePage import BasePage


class CaseFlagsPages(BasePage):
    SET_FLAGS_BUTTON_ID = "button-Set flags"
    FLAG_INPUT = ".tokenfield-input"

    def select_flag(self, flag_name):
        flag = self.driver.find_element_by_css_selector(self.FLAG_INPUT)
        flag.send_keys(flag_name)
        self.driver.find_element_by_id(self.SET_FLAGS_BUTTON_ID).click()
