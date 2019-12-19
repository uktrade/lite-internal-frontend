from shared.BasePage import BasePage


class CaseFlagsPages(BasePage):
    def select_flag(self, flag_id):
        flag = self.driver.find_elements_by_id(flag_id)[0]
        flag.click()
