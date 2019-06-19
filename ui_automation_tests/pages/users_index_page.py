class UsersIndexPage():

    def __init__(self, driver):
        self.driver = driver
        self.add_user_button = ".govuk-button[href*='users/add']" #css

    def click_add_a_user_button(self):
        self.driver.find_element_by_css_selector(self.add_user_button).click()