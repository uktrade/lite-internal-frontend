from selenium.webdriver.support.ui import Select


class CaseFlagsPages():

    def __init__(self, driver):
        self.driver = driver

    def assign_flags(self, value):
        select = Select(self.driver.find_element_by_id('level'))
        select.select_by_visible_text(value)
