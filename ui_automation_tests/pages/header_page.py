class HeaderPage():

    def __init__(self, driver):
        self.driver = driver
        self.menu_button = "lite-user-menu-button" #id

    def click_lite_menu(self):
        self.driver.find_element_by_id(self.menu_button).click()

    def click_organisations(self):
        self.driver.find_element_by_css_selector("a[href*='/organisations/']").click()

    def click_teams(self):
        self.driver.find_element_by_css_selector("a[href*='/teams/']").click()

