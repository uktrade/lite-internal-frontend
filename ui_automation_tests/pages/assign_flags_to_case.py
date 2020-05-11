from shared.BasePage import BasePage


class CaseFlagsPages(BasePage):
    def select_flag(self, flag_name):
        self.driver.find_element_by_id(flag_name.replace(" ", "-")).click()
