from selenium.webdriver.support.select import Select

import shared.tools.helpers as utils
from shared.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_below_header_by_id


class CompliancePages(BasePage):

    def find_case_reference(self, context):
        return self.driver.find_element_by_link_text(context.reference_code).text
