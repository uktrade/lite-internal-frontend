from selenium.webdriver.support.select import Select
from shared.BasePage import BasePage

from shared import functions


class CompliancePages(BasePage):

    CASE_REFERENCE_ID = "reference"
    ADD_VISIT_REPORT_ID = "add-visit-report"
    EDIT_VISIT_REPORT_DETAILS_ID = "edit-visit-report-details"
    VISIT_TYPE_ID = "visit_type"
    OVERALL_RISK_VALUE_ID = "overall_risk_value"
    LICENCE_RISK_VALUE_ID = "licence_risk_value"
    EDIT_OVERVIEW_ID = "edit-overview"
    OVERVIEW_ID = "overview"
    EDIT_INSPECTION_ID = "edit-inspection"
    INSPECTION_ID = "inspection"
    EDIT_COMPLIANCE_WITH_LICENCES_ID = "edit-compliance-with-licences"
    COMPLIANCE_WITH_LICENCE_OVERVIEW_ID = "compliance_overview"
    COMPLIANCE_WITH_LICENCE_RISK_VALUE_ID = "compliance_risk_value"
    EDIT_KNOWLEDGE_OF_INDIVIDUALS_ID = "edit-knowledge-of-individuals"
    KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID = "individuals_overview"
    KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID = "individuals_risk_value"
    EDIT_KNOWLEDGE_OF_PRODUCTS_ID = "edit-knowledge-of-products"
    KNOWLEDGE_OF_PRODUCTS_OVERVIEW_ID = "products_overview"
    KNOWLEDGE_OF_PRODUCTS_RISK_VALUE_ID = "products_risk_value"

    def find_case_reference(self, context):
        return self.driver.find_element_by_link_text(context.reference_code)

    def filter_by_case_reference(self, context):
        self.driver.find_element_by_id(self.CASE_REFERENCE_ID).send_keys(context.reference_code)

    def add_visit_report(self):
        self.driver.find_element_by_id(self.ADD_VISIT_REPORT_ID).click()

    def add_visit_report_details(self, visit_type, visit_date, overall_risk, licence_risk):
        self.driver.find_element_by_id(self.EDIT_VISIT_REPORT_DETAILS_ID).click()
        Select(self.driver.find_element_by_id(self.VISIT_TYPE_ID)).select_by_visible_text(visit_type)

        # date field

        Select(self.driver.find_element_by_id(self.OVERALL_RISK_VALUE_ID)).select_by_visible_text(overall_risk)

        Select(self.driver.find_element_by_id(self.LICENCE_RISK_VALUE_ID)).select_by_visible_text(licence_risk)

        functions.click_submit(self.driver)

    def get_visit_type(self):
        return self.driver.find_element_by_id(self.VISIT_TYPE_ID).text

    def get_visit_date(self):
        return self.driver.find_element_by_id(self.VISIT_DATE_ID).text

    def get_overall_risk(self):
        return self.driver.find_element_by_id(self.OVERALL_RISK_VALUE_ID).text

    def get_licence_risk(self):
        return self.driver.find_element_by_id(self.LICENCE_RISK_VALUE_ID).text

    def edit_overview(self, text):
        self.driver.find_element_by_id(self.EDIT_OVERVIEW_ID).click()
        self.driver.find_element_by_id(self.OVERVIEW_ID).send_keys(text)
        functions.click_submit(self.driver)

    def get_overview(self):
        return self.driver.find_element_by_id(self.OVERVIEW_ID).text

    def edit_inspection(self, text):
        self.driver.find_element_by_id(self.EDIT_INSPECTION_ID).click()
        self.driver.find_element_by_id(self.INSPECTION_ID).send_keys(text)
        functions.click_submit(self.driver)

    def get_inspection(self):
        return self.driver.find_element_by_id(self.INSPECTION_ID).text

    def edit_compliance_with_licences(self, overview, risk_value):
        self.driver.find_element_by_id(self.EDIT_COMPLIANCE_WITH_LICENCES_ID).click()
        self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_OVERVIEW_ID).send_keys(overview)
        Select(self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_RISK_VALUE_ID)).select_by_visible_text(
            risk_value
        )
        functions.click_submit(self.driver)

    def get_compliance_with_licence_overview(self):
        return self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_OVERVIEW_ID).text

    def get_compliance_with_licence_risk(self):
        return self.driver.find_element_by_id(self.COMPLIANCE_WITH_LICENCE_RISK_VALUE_ID).text

    def edit_knowledge_of_individuals(self, overview, risk_value):
        self.driver.find_element_by_id(self.EDIT_KNOWLEDGE_OF_INDIVIDUALS_ID).click()
        self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID).send_keys(overview)
        Select(self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID)).select_by_visible_text(
            risk_value
        )
        functions.click_submit(self.driver)

    def get_knowledge_of_individuals_overview(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID).text

    def get_knowledge_of_individuals_risk(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID).text

    def edit_knowledge_of_products(self, overview, risk_value):
        self.driver.find_element_by_id(self.EDIT_KNOWLEDGE_OF_PRODUCTS_ID).click()
        self.driver.find_element_by_id(self.KNOWLEDGE_OF_PRODUCTS_OVERVIEW_ID).send_keys(overview)
        Select(self.driver.find_element_by_id(self.KNOWLEDGE_OF_PRODUCTS_RISK_VALUE_ID)).select_by_visible_text(
            risk_value
        )
        functions.click_submit(self.driver)

    def get_knowledge_of_products_overview(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_OVERVIEW_ID).text

    def get_knowledge_of_products_risk(self):
        return self.driver.find_element_by_id(self.KNOWLEDGE_OF_INDIVIDUALS_RISK_VALUE_ID).text
