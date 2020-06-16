from selenium.webdriver.support.select import Select

import shared.tools.helpers as utils
from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_below_header_by_id


class CompliancePages(BasePage):
    GENERATE_DECISION_DOCUMENT_BUTTON_ID = "generate-document-approve"
    DOCUMENT_TEMPLATE_CSS = ".govuk-label"
    LINK_TO_LICENCE_ID = "link-to-licence-"

    def select_generate_document(self):
        self.driver.find_element_by_id(self.GENERATE_DECISION_DOCUMENT_BUTTON_ID).click()

    def select_document_template(self):
        self.driver.find_element_by_css_selector(self.DOCUMENT_TEMPLATE_CSS).click()

    def find_case_text(self, context):
        return self.driver.find_element_by_link_text(context.reference_code).text
