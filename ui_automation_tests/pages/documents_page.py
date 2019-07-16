class DocumentsPage():

    def __init__(self, driver):
        self.driver = driver
        self.attach_docs_btn = '.govuk-button[href*="attach"]' #css
        self.latest_filename =  '//*[@id="main-content"]/div[2]/div[1]/p[1]' #xpath
        self.second_latest_filename =  '//*[@id="main-content"]/div[3]/div[1]/p[1]' #xpath
        self.latest_file_description =  '//*[@id="main-content"]/div[2]/div[1]/p[2]' #xpath
        self.second_latest_file_description = '//*[@id="main-content"]/div[3]/div[1]/p[2]' #xpath

    def click_attach_documents(self):
        return self.driver.find_element_by_css_selector(self.attach_docs_btn).click()

    def get_latest_file_name(self):
        return self.driver.find_element_by_xpath(self.latest_filename).text

    def get_second_latest_file_name(self):
        return self.driver.find_element_by_xpath(self.second_latest_filename).text

    def get_latest_file_description(self):
        return self.driver.find_element_by_xpath(self.latest_file_description).text

    def get_second_latest_file_description(self):
        return self.driver.find_element_by_xpath(self.second_latest_file_description).text
