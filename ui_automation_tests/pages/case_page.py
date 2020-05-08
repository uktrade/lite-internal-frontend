from shared import selectors
from shared.BasePage import BasePage


class CaseTabs:
    DETAILS = "details"
    USER_ADVICE = "user-advice"
    TEAM_ADVICE = "team-advice"
    FINAL_ADVICE = "final-advice"
    ADDITIONAL_CONTACTS = "additional-contacts"
    ECJU_QUERIES = "ecju-queries"
    DOCUMENTS = "documents"
    ACTIVITY = "activity"


class CasePage(BasePage):
    TABLE_GOODS_ID = "table-goods"
    TABLE_DESTINATIONS_ID = "table-destinations"

    AUDIT_TRAIL_ID = "audit-trail"

    BUTTON_RERUN_ROUTING_RULES_ID = "button-rerun-routing-rules"

    LINK_CHANGE_STATUS_ID = "link-change-status"
    LINK_CHANGE_CASE_FLAGS_ID = "link-change-flags"
    LINK_ASSIGN_CASE_OFFICER_ID = "link-change-case-officer"
    LINK_ASSIGN_USERS_ID = "link-change-assigned-users"

    def change_tab(self, tab: str):
        if tab == CaseTabs.USER_ADVICE or tab == CaseTabs.TEAM_ADVICE or tab == CaseTabs.FINAL_ADVICE:
            self.driver.find_element_by_id("tab-collection-advice").click()

        self.driver.find_element_by_id("tab-" + tab).click()

    def click_change_case_flags(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_CASE_FLAGS_ID).click()

    def click_assign_case_officer(self):
        self.driver.find_element_by_id(self.LINK_ASSIGN_CASE_OFFICER_ID).click()

    def click_assign_users(self):
        self.driver.find_element_by_id(self.LINK_ASSIGN_USERS_ID).click()

    def click_change_status(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_STATUS_ID).click()

    def click_rerun_routing_rules(self):
        self.driver.find_element_by_id(self.BUTTON_RERUN_ROUTING_RULES_ID).click()

    def select_goods(self):
        for good in self.driver.find_elements_by_css_selector(f"#{self.TABLE_GOODS_ID} {selectors.CHECKBOX}"):
            good.click()

    def get_goods_text(self):
        return self.driver.find_element_by_id(self.TABLE_GOODS_ID).text

    def get_destinations_text(self):
        return self.driver.find_element_by_id(self.TABLE_DESTINATIONS_ID).text

    def select_destinations(self):
        for destination in self.driver.find_elements_by_css_selector(self.TABLE_DESTINATIONS_ID + selectors.CHECKBOX):
            destination.click()

    def get_audit_trail_text(self):
        return self.driver.find_element_by_id(self.AUDIT_TRAIL_ID).text
