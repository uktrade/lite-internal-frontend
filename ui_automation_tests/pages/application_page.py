from selenium.webdriver.support.ui import Select
import time

from helpers.BasePage import BasePage
from selenium.common.exceptions import NoSuchElementException


class ApplicationPage(BasePage):

    ACTIONS_DROPDOWN = ".app-more-actions__button"  # CSS
    CASE_NOTIFICATION_ANCHOR = "case-notification"  # ID
    AUDIT_ID = "[id^=case-activity-]"  # CSS
    CASE_NOTE_FIELD = "case_note"  # id
    POST_NOTE_BTN = "button-post-note"  # id
    CANCEL_NOTE_BTN = "case-note-cancel-button"  # id
    CASE_NOTES_TEXT = ".app-activity__additional-text"  # css
    CASE_NOTE_DATE_TIME = ".app-activity__item .govuk-hint"  # css
    CASE_NOTE_CHARACTER_WARNING = "case_note-warning"  # id
    DOCUMENTS_BTN = '[href*="documents"]'  # css
    ECJU_QUERIES_BTN = '[href*="ecju-queries"]'  # css
    PROGRESS_APP_BTN = '[href*="manage"]'
    RECORD_DECISION_BTN = '[href*="decide"]'  # css
    HEADERS = ".lite-heading-s"  # css
    ACTIVITY_CASE_NOTE_SUBJECT = ".govuk-body"
    ACTIVITY_DATES = ".app-activity__item .govuk-hint"
    ACTIVITY_USER = ".user"
    IS_VISIBLE_TO_EXPORTER_CHECKBOX_ID = "is_visible_to_exporter"
    REVIEW_GOODS = "button-review-goods"
    EDIT_CASE_FLAGS = "application-edit-case-flags"  # ID
    CHECKBOX_INPUT = ".govuk-checkboxes__input"
    VIEW_ADVICE = 'a[href*="/user-advice-view/"]'
    CASE_FLAGS = "application-case-flags"
    MOVE_CASE_BUTTON = '[href*="move"]'  # CSS
    STATUS = "status"  # ID
    AUDIT_TRAIL_ITEM = ".app-activity__item"  # CSS
    APPLICATION_SUMMARY_BOARD = ".govuk-summary-list"  # CSS
    EU_TABLE = "end-user"  # ID
    UEU_TABLE = "ultimate-end-users"  # ID
    CONSIGNEE_TABLE = "consignee"  # ID
    THIRD_PARTIES_TABLE = "third-parties"  # ID
    GIVE_ADVICE_BUTTON = "button-give-advice"  # ID
    CHECKBOX = '[type="checkbox"]'  # CSS
    DOWNLOAD_GOOD_DOCUMENT = "good_document"  # ID
    DOWNLOAD_END_USER_DOCUMENT = "end_user_document"  # ID
    DOWNLOAD_ADDITIONAL_DOCUMENT = "additional_document"  # ID
    ORGANISATION = "applicant_organisation"  # CSS
    EDIT_GOODS_FLAGS = "button-edit-goods-flags"  # ID

    GOODS_DESCRIPTION_LINK = "#goods a"  # CSS

    def click_visible_to_exporter_checkbox(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.IS_VISIBLE_TO_EXPORTER_CHECKBOX_ID).click()

    def enter_case_note(self, text):
        self.driver.execute_script(f'document.getElementById("{self.CASE_NOTE_FIELD}").value = "{text[:-1]}"')
        self.driver.find_element_by_id(self.CASE_NOTE_FIELD).send_keys(text[-1:])

    def get_text_of_case_note_field(self):
        return self.driver.find_element_by_id(self.CASE_NOTE_FIELD).text

    def click_post_note_btn(self):
        self.driver.find_element_by_id(self.POST_NOTE_BTN).click()

    def click_cancel_btn(self):
        time.sleep(0.5)
        self.driver.find_element_by_id(self.CANCEL_NOTE_BTN).click()

    def get_text_of_case_note(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTES_TEXT)[no].text

    def get_text_of_case_note_date_time(self, no):
        return self.driver.find_elements_by_css_selector(self.CASE_NOTE_DATE_TIME)[no].text

    def get_text_of_case_note_warning(self):
        time.sleep(1)
        return self.driver.find_element_by_id(self.CASE_NOTE_CHARACTER_WARNING).text

    def get_disabled_attribute_of_post_note(self):
        return self.driver.find_element_by_id(self.POST_NOTE_BTN).get_attribute("disabled")

    def get_class_name_of_post_note(self):
        return self.driver.find_element_by_id(self.POST_NOTE_BTN).get_attribute("class")

    def click_progress_application(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.PROGRESS_APP_BTN).click()

    def click_record_decision(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.RECORD_DECISION_BTN).click()

    def click_documents_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.DOCUMENTS_BTN).click()

    def click_ecju_queries_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.ECJU_QUERIES_BTN).click()

    def click_drop_down(self):
        self.driver.find_element_by_css_selector(self.ACTIONS_DROPDOWN).click()

    def select_status(self, status):
        case_status_dropdown = Select(self.driver.find_element_by_id(self.STATUS))
        case_status_dropdown.select_by_visible_text(status)

    def get_text_of_case_note_subject(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_CASE_NOTE_SUBJECT)[no].text

    def get_text_of_activity_dates(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_DATES)[no].text

    def get_text_of_activity_users(self, no):
        return self.driver.find_elements_by_css_selector(self.ACTIVITY_USER)[no].text

    def click_review_goods(self):
        self.driver.find_element_by_id(self.REVIEW_GOODS).click()

    def is_review_goods_button_present(self):
        try:
            self.driver.find_element_by_id(self.REVIEW_GOODS)
            return True
        except NoSuchElementException:
            return False

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.EDIT_GOODS_FLAGS)
        edit_goods_btn.click()

    def click_edit_case_flags(self):
        edit_cases_btn = self.driver.find_element_by_id(self.EDIT_CASE_FLAGS)
        edit_cases_btn.click()

    def select_a_good(self):
        element = self.driver.find_element_by_css_selector(self.CHECKBOX_INPUT)
        self.driver.execute_script("arguments[0].click();", element)

    def click_view_advice(self):
        self.driver.find_element_by_css_selector(self.ACTIONS_DROPDOWN).click()
        self.driver.find_element_by_css_selector(self.VIEW_ADVICE).click()

    def is_flag_applied(self, flag_id):
        count = len(self.driver.find_elements_by_id(flag_id))
        return count > 0

    def is_good_flag_applied(self, flag_name):
        return flag_name in self.driver.find_element_by_id("goods").text

    def click_move_case_button(self):
        self.click_drop_down()
        self.driver.find_element_by_css_selector(self.MOVE_CASE_BUTTON).click()

    def get_text_of_audit_trail_item(self, no):
        return self.driver.find_elements_by_css_selector(self.AUDIT_TRAIL_ITEM)[no].text

    def get_text_of_application_summary_board(self):
        return self.driver.find_element_by_css_selector(self.APPLICATION_SUMMARY_BOARD).text

    def get_text_of_eu_table(self):
        return self.driver.find_element_by_id(self.EU_TABLE).text

    def get_case_notification_anchor(self):
        return self.driver.find_element_by_id(self.CASE_NOTIFICATION_ANCHOR)

    def get_case_activity_id_by_audit_text(self, audit_text):
        audits = self.driver.find_elements_by_css_selector(self.AUDIT_ID)
        for audit in audits:
            if audit_text in audit.text:
                return audit.get_attribute("id")

        return None

    def get_text_of_ueu_table(self):
        return self.driver.find_element_by_id(self.UEU_TABLE).text

    def get_text_of_consignee_table(self):
        return self.driver.find_element_by_id(self.CONSIGNEE_TABLE).text

    def get_text_of_third_parties_table(self):
        return self.driver.find_element_by_id(self.THIRD_PARTIES_TABLE).text

    def click_on_all_checkboxes(self):
        elements = self.driver.find_elements_by_css_selector(self.CHECKBOX)
        num = 0
        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)
            num += 1
        self.driver.find_element_by_id(self.GIVE_ADVICE_BUTTON).click()
        return num

    def good_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_GOOD_DOCUMENT).is_enabled()

    def end_user_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_END_USER_DOCUMENT).is_enabled()

    def get_case_flag_element(self):
        return self.driver.find_element_by_id(self.CASE_FLAGS)

    def get_document_element(self):
        return self.driver.find_element_by_css_selector(self.DOCUMENTS_BTN)

    def get_move_case_element(self):
        return self.driver.find_element_by_css_selector(self.MOVE_CASE_BUTTON)

    def get_ecju_queries_element(self):
        return self.driver.find_element_by_css_selector(self.ECJU_QUERIES_BTN)

    def is_change_status_available(self):
        # this should equal 2 as there is a 'manage' in the link of the footer image
        return len(self.driver.find_elements_by_css_selector(self.PROGRESS_APP_BTN)) == 2

    def additional_document_link_is_enabled(self):
        return self.driver.find_element_by_id(self.DOWNLOAD_ADDITIONAL_DOCUMENT).is_enabled()

    def go_to_organisation(self):
        element = self.driver.find_element_by_id(self.ORGANISATION)
        self.driver.execute_script("arguments[0].click();", element)

    def click_good_description_link(self):
        element = self.driver.find_element_by_css_selector(self.GOODS_DESCRIPTION_LINK)
        self.driver.execute_script("arguments[0].click();", element)
