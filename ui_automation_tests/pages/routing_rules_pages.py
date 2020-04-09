from selenium.webdriver.support.select import Select
from shared.BasePage import BasePage

from ui_automation_tests.shared import functions


class RoutingRulesPage(BasePage):
    TEXT_TIER_ID = "tier"
    TEXT_QUEUE_ID = "queue"
    TEXT_COUNTRY_ID = "country"
    SELECT_CASE_STATUS_ID = "status"
    BTN_CREATE_NEW_ROUTING_RULE = "create-routing-rule"
    REACTIVATE_ROUTING_RULE_BUTTON = "a[href*='/reactivate/']"  # CSS
    DEACTIVATE_ROUTING_RULE_BUTTON = "a[href*='/deactivate/']"  # CSS
    CONFIRM_DEACTIVATE_REACTIVATE = "confirm-yes"
    CHECKBOX_ADDITIONAL_RULES = "input[name='additional_rules[]'][type='checkbox']"  # CSS
    SELECT_FLAG_ID = "flag"
    CHECKBOX_AND_LABEL = "[class=govuk-checkboxes__item]"

    def create_new_routing_rule(self):
        self.driver.find_element_by_id(self.BTN_CREATE_NEW_ROUTING_RULE).click()

    def initial_details_form(self, case_status=None, queue=None, tier=None, additional_rules=None):
        if case_status:
            self.select_case_status(case_status)

        if queue:
            self.enter_queue(queue)

        if tier:
            self.enter_tier(tier)

        if additional_rules:
            self.select_all_additional_rules()
        else:
            self.select_no_additional_rules()

    def select_all_additional_rules(self):
        rules = self.driver.find_elements_by_css_selector(self.CHECKBOX_ADDITIONAL_RULES)
        for rule in rules:
            if not rule.is_selected():
                rule.click()

    def select_no_additional_rules(self):
        rules = self.driver.find_elements_by_css_selector(self.CHECKBOX_ADDITIONAL_RULES)
        for rule in rules:
            if rule.is_selected():
                rule.click()

    def enter_queue(self, text):
        functions.send_keys_to_autocomplete(self.driver, self.TEXT_QUEUE_ID, text)

    def select_case_status(self, status):
        select = Select(self.driver.find_element_by_id(self.SELECT_CASE_STATUS_ID))
        select.select_by_visible_text(status)

    def enter_tier(self, text):
        self.driver.find_element_by_id(self.TEXT_TIER_ID).clear()
        self.driver.find_element_by_id(self.TEXT_TIER_ID).send_keys(text)

    def select_case_type_by_text(self, text):
        checkbox_parents = self.driver.find_elements_by_css_selector("[class=govuk-checkboxes__item]")
        for parent in checkbox_parents:
            if parent.text == text:
                parent.find_element_by_css_selector("input").click()
                break

    def select_flag(self, flag_name):
        checkbox_parents = self.driver.find_elements_by_css_selector("[class=govuk-checkboxes__item]")
        for parent in checkbox_parents:
            if parent.text == flag_name:
                parent.find_element_by_css_selector("input").click()
                break

    def enter_country(self, country):
        functions.send_keys_to_autocomplete(self.driver, self.TEXT_COUNTRY_ID, country)

    def select_first_user(self):
        self.driver.find_element_by_css_selector("input[class=govuk-radios__input]").click()

    def click_on_deactivate_rule(self, element):
        element.find_element_by_css_selector(self.DEACTIVATE_ROUTING_RULE_BUTTON).click()

    def click_confirm_deactivate_activate(self):
        self.driver.find_element_by_id(self.CONFIRM_DEACTIVATE_REACTIVATE).click()

    def click_on_reactivate_rule(self):
        self.driver.find_element_by_css_selector(self.REACTIVATE_FLAG_BUTTON).click()
