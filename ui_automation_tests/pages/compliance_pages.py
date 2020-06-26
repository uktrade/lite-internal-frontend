from shared.BasePage import BasePage


class CompliancePages(BasePage):

    CASE_REFERENCE_ID = "reference"
    ADD_VISIT_REPORT_ID = "add-visit-report"

    def find_case_reference(self, context):
        return self.driver.find_element_by_link_text(context.reference_code)

    def filter_by_case_reference(self, context):
        self.driver.find_element_by_id(self.CASE_REFERENCE_ID).send_keys(context.reference_code)

    def add_visit_report(self):
        self.driver.find_element_by_id(self.ADD_VISIT_REPORT_ID).click()

    def add_visit_report_details(self, visit_type, visit_date, overall_risk, licence_risk):
        self.driver
