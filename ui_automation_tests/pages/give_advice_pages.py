from selenium.webdriver.support.select import Select

from shared.BasePage import BasePage

from ui_automation_tests.shared.functions import element_with_id_exists


class GiveAdvicePages(BasePage):
    ADVICE_CHECKBOX_OPTION = "type-"  # ID
    PICKLIST_ITEM_TEXT = ".app-picklist-picker__item p"  # CSS
    TEXTAREA_NOTES_ID = "note"
    TEAM_ADVICE = "team_advice"
    FINAL_ADVICE = "final_advice"
    COMBINE_ADVICE_BUTTON = "combine_advice_button"
    CLEAR_ADVICE_BUTTON = "button-clear-advice"
    FINALISE_BUTTON = "button-finalise"
    GIVE_OR_CHANGE_ADVICE_BUTTON = "button-give-advice"
    FINALISE_GOODS_AND_COUNTRIES_BUTTON = "button-finalise"
    CLEARANCE_LEVEL_DROPDOWN_ID = "pv_grading_proviso"
    RADIO_INPUT_APPROVE = '.govuk-radios input[value="approve"]'
    BLOCKING_FLAGS_WARNING_ID = "blocking_flags"

    def click_on_advice_option(self, option):
        self.driver.find_element_by_id(self.ADVICE_CHECKBOX_OPTION + option).click()

    def click_on_clear_advice(self):
        self.driver.find_element_by_id(self.CLEAR_ADVICE_BUTTON).click()

    def click_on_import_link(self, option):
        self.driver.find_element_by_id(f"link-{option}-picklist-picker").click()

    def click_on_picklist_item(self, option):
        self.driver.execute_script('document.getElementById("picklist-' + option + '").children[0].click()')
        self.driver.execute_script('document.getElementById("button-submit").click()')

    def get_text_of_picklist_item(self):
        return self.driver.find_element_by_css_selector(self.PICKLIST_ITEM_TEXT).text

    def type_in_additional_note_text_field(self, text):
        return self.driver.find_element_by_id(self.TEXTAREA_NOTES_ID).send_keys(text)

    def combine_advice(self):
        self.driver.find_element_by_id(self.COMBINE_ADVICE_BUTTON).click()

    def finalise(self):
        self.driver.find_element_by_id(self.FINALISE_BUTTON).click()

    def can_finalise(self):
        return element_with_id_exists(self.driver, self.FINALISE_BUTTON)

    def finalise_goods_and_countries(self):
        self.driver.find_element_by_id(self.FINALISE_GOODS_AND_COUNTRIES_BUTTON).click()

    def select_approve_for_all(self):
        elements = self.driver.find_elements_by_css_selector(self.RADIO_INPUT_APPROVE)
        for element in elements:
            self.driver.execute_script("arguments[0].click();", element)

    def checkbox_present(self):
        return len(self.driver.find_elements_by_css_selector(".input"))

    def give_advice_button_present(self):
        return self.driver.find_elements_by_id(self.GIVE_OR_CHANGE_ADVICE_BUTTON)

    def clearance_grading_present(self):
        return self.driver.find_elements_by_id(self.CLEARANCE_LEVEL_DROPDOWN_ID)

    def select_clearance_grading(self, clearance_level):
        Select(self.driver.find_element_by_id(self.CLEARANCE_LEVEL_DROPDOWN_ID)).select_by_visible_text(clearance_level)

    def get_blocking_flags_text(self):
        return self.driver.find_element_by_id(self.BLOCKING_FLAGS_WARNING_ID).text
