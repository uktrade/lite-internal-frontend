from helpers.BasePage import BasePage


class ClcQueriesPages(BasePage):

    respond_to_query_btn = '.govuk-button[href*="respond-to-query"]'  # css
    control_response = 'is_good_controlled-'  # id
    control_code = 'control_code'
    report_summary = '(//div[@class="govuk-radios__item"]//input[@name="report_summary"])'  # xpath
    comment = 'comment'  # id
    case_close = '.lite-info-bar'  # css
    submit_button = '.govuk-button[type*="submit"]'

    def respond_to_query(self):
        self.driver.find_element_by_css_selector(self.respond_to_query_btn).click()

    # Response Page
    def is_good_controlled(self, answer):
        self.driver.find_element_by_id(self.control_response + answer).click()

    def control_code_response(self, code):
        self.driver.find_element_by_id(self.control_code).send_keys(code)

    def choose_report_summary(self, num):
        self.driver.find_elements_by_xpath(self.report_summary)[int(num)].click()

    def enter_a_comment(self, comment):
        self.driver.find_element_by_id(self.comment).send_keys(comment)

    def case_closed(self):
        return len(self.driver.find_elements_by_css_selector(self.case_close)) == 1

    def click_submit(self):
        self.driver.find_element_by_css_selector(self.submit_button).click()
