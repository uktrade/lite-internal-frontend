from helpers.BasePage import BasePage


class OrganisationsPage(BasePage):

    # called e time you create an object for this class

    def click_new_organisation_btn(self):
        new_organisation_btn = self.driver.find_element_by_css_selector("a[href*='organisations/register']")
        new_organisation_btn.click()
