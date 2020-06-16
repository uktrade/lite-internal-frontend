from shared.BasePage import BasePage


class CompliancePages(BasePage):
    def find_case_reference(self, context):
        return self.driver.find_element_by_link_text(context.reference_code)
