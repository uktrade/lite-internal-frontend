from shared import functions
from shared.BasePage import BasePage
from selenium.webdriver.support.ui import Select


class GoodsQueriesPages(BasePage):
    CONTROL_RESPONSE = "is_good_controlled-"  # ID
    TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR = "#pane_control_list_entries .tokenfield-input"
    REPORT_SUMMARY = "report_summary"  # Name
    COMMENT = "comment"  # ID
    CASE_CLOSE_INFO_BAR_ID = "banner-case-closed"
    BUTTON_CLC_RESPOND_ID = "clc-button-respond"
    BUTTON_GRADING_RESPOND_ID = "grading-button-respond"
    SUBMIT_BUTTON = '.govuk-button[type*="submit"]'  # CSS
    PREFIX_ID = "prefix"
    GRADING_ID = "grading"

    def click_respond_to_clc_query(self):
        self.driver.find_element_by_id(self.BUTTON_CLC_RESPOND_ID).click()

    def click_respond_to_grading_query(self):
        self.driver.find_element_by_id(self.BUTTON_GRADING_RESPOND_ID).click()

    # Response Page
    def click_is_good_controlled(self, answer):
        self.driver.find_element_by_id(self.CONTROL_RESPONSE + answer).click()

    def type_in_to_control_list_entry(self, code):
        functions.send_tokens_to_token_bar(self.driver, self.TOKEN_BAR_CONTROL_LIST_ENTRIES_SELECTOR, [code])

    def choose_report_summary(self, num):
        element = self.driver.find_elements_by_name(self.REPORT_SUMMARY)[int(num)]
        self.driver.execute_script("arguments[0].click();", element)

    def enter_a_comment(self, comment):
        self.driver.find_element_by_class_name("govuk-details__summary-text").click()
        self.driver.find_element_by_id(self.COMMENT).send_keys(comment)

    def enter_a_prefix(self, prefix):
        self.driver.find_element_by_id(self.PREFIX_ID).send_keys(prefix)

    def select_a_grading(self, grading):
        Select(self.driver.find_element_by_id(self.GRADING_ID)).select_by_visible_text(grading)

    def enter_a_suffix(self, suffix):
        self.driver.find_element_by_id(self.COMMENT).send_keys(suffix)

    def is_clc_query_case_closed(self):
        return len(self.driver.find_elements_by_id(self.CASE_CLOSE_INFO_BAR_ID)) == 1
