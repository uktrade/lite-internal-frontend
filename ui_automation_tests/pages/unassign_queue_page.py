from ui_automation_tests.shared.BasePage import BasePage


class UnassignQueuePage(BasePage):
    QUEUE_CHECKBOX_CSS = ".govuk-checkboxes__input"

    def check_unassign_checkbox(self):
        self.driver.find_element_by_css_selector(self.QUEUE_CHECKBOX_CSS).click()
