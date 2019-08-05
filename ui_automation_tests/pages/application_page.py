from selenium.webdriver.support.ui import Select
import time


class ApplicationPage():

    def __init__(self, driver):
        self.driver = driver

        self.case_note_field = "case_note"  # id
        self.post_note_btn = "button-post-note"  # id
        self.cancel_note_btn = "case-note-cancel-button"  # id
        self.case_notes_text = ".lite-case-note"  # css
        self.case_note_date_time = ".lite-activity-item .govuk-hint"  # css
        self.case_note_character_warning = "case_note-warning"  # id
        self.documents_btn = '.govuk-button[href*="documents"]'  # css
        self.progress_app_btn = '.govuk-button[href*="manage"]'
        self.record_decision_btn = '.govuk-button[href*="decide"]'  # css
        self.headers = ".lite-heading-s"  # css
        self.activity_case_note_subject = ".lite-activity-item .govuk-body"
        self.activity_dates = ".lite-activity-item .govuk-hint"
        self.activity_user = ".user"
        self.is_visible_to_exporter_checkbox_id = 'is_visible_to_exporter'
        self.edit_case_flags = "a[href*='/assign-flags']"
        self.advice_view = "a[href*='/advice-view/']"
        self.case_flags = 'application-case-flags'

    def click_visible_to_exporter_checkbox(self):
        self.driver.find_element_by_id(self.is_visible_to_exporter_checkbox_id).click()

    def enter_case_note(self, text):
        self.driver.find_element_by_id(self.case_note_field).send_keys(text)

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.case_note_field).text

    def click_post_note_btn(self):
        self.driver.find_element_by_id(self.post_note_btn).click()

    def click_cancel_btn(self):
        self.driver.find_element_by_id(self.cancel_note_btn).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.case_notes_text)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.case_note_date_time)[no].text

    def get_text_of_case_note_warning(self):
        time.sleep(1)
        return self.driver.find_element_by_id(self.case_note_character_warning).text

    def get_disabled_attribute_of_post_note(self):
        return self.driver.find_element_by_id(self.post_note_btn).get_attribute("disabled")

    def click_progress_application(self):
        self.driver.find_element_by_css_selector(self.progress_app_btn).click()

    def click_record_decision(self):
        self.driver.find_element_by_css_selector(self.record_decision_btn).click()

    def click_documents_button(self):
        self.driver.find_element_by_css_selector(self.documents_btn).click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id('status'))
        time.sleep(1)
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_application_headings(self):
        return self.driver.find_elements_by_css_selector(self.headers)

    def get_text_of_case_note_subject(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_case_note_subject)[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_dates)[no].text

    def get_text_of_activity_users(self, no):
        return self.driver.find_elements_by_css_selector(self.activity_user)[no].text

    def click_edit_case_flags(self):
        edit_cases_btn = self.driver.find_element_by_id(self.edit_case_flags)
        edit_cases_btn.click()


    def click_view_adivce(self):
        self.driver.find_element_by_css_selector(self.advice_view).click()


    def is_flag_applied(self, flag_id):
        case_flags = self.driver.find_element_by_id(self.case_flags)
        count = len(case_flags.find_elements_by_id(flag_id))
        return count == 1
