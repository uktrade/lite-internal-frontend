class DepartmentOfInternationalTradeHub():

    # called e time you create an object for this class
    def __init__(self, driver):
        self.driver = driver

        self.url = "http://localhost:7000/"
        self.manage_cases_btn = "a[href*='/cases']"
        self.manage_organisations_btn = "a[href*='/organisations']"

    def go_to(self):
        self.driver.get(self.url)

    def click_manage_cases_btn(self):
        self.driver.find_element_by_css_selector(self.manage_cases_btn).click()

    def click_manage_organisations_btn(self):
        self.driver.find_element_by_css_selector(self.manage_organisations_btn).click()

