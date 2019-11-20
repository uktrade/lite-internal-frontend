from helpers.BasePage import BasePage
from shared.tools.helpers import scroll_to_element_by_id, scroll_to_bottom_of_page


class OrganisationPage(BasePage):

    LINK_ORGANISATION_FLAGS_ID = "link-organisation-flags"
    flags_area = ".app-flag"

    def click_edit_organisation_flags(self):
        # scroll_to_element_by_id(self.driver, self.LINK_ORGANISATION_FLAGS_ID)
        scroll_to_bottom_of_page(self.driver)
        self.driver.find_element_by_id(self.LINK_ORGANISATION_FLAGS_ID).click()

    def is_organisation_flag_applied(self, flag_name):
        elements = self.driver.find_elements_by_css_selector(self.flags_area)
        for element in elements:
            if flag_name in element.text:
                return True
        return False
