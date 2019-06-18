class Shared():

    def __init__(self, driver):
        self.driver = driver
        self.submit_button = "[type*='submit']"

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()
