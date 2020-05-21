from shared import functions
from shared.BasePage import BasePage


class OpenGeneralLicencesListPage(BasePage):
    BUTTON_NEW_OGL_ID = "button-new-ogl"
    INPUT_NAME_ID = "name"
    LINK_VIEW_SELECTOR = ".govuk-table__cell:last-of-type a"

    def click_new_open_general_licence_button(self):
        self.driver.find_element_by_id(self.BUTTON_NEW_OGL_ID).click()

    def filter_by_name(self, name):
        functions.try_open_filters(self.driver)
        self.driver.find_element_by_id(self.INPUT_NAME_ID).send_keys(name)
        self.driver.find_element_by_id("button-apply-filters").click()

    def click_view_first_ogl_link(self):
        self.driver.find_element_by_css_selector(self.LINK_VIEW_SELECTOR).click()


class OpenGeneralLicencesDetailPage(BasePage):
    SUMMARY_LIST_CLASS = "govuk-summary-list"

    def get_summary_list_text(self):
        return self.driver.find_element_by_class_name(self.SUMMARY_LIST_CLASS).text


class OpenGeneralLicencesCreatePage(BasePage):
    RADIO_OPEN_GENERAL_EXPORT_LICENCE_ID = "case_type-00000000-0000-0000-0000-000000000002"
    INPUT_NAME_ID = "name"
    INPUT_DESCRIPTION_ID = "description"
    INPUT_LINK_ID = "url"
    RADIO_REGISTRATION_REQUIRED_YES_ID = "registration_required-True"
    TREE_CONTROLLED_RADIOACTIVE_ID = "node-Controlled-Radioactive-Sources"
    CHECKBOX_UNITED_KINGDOM_ID = "United-Kingdom"

    def select_open_general_export_licence_radiobutton(self):
        self.driver.find_element_by_id(self.RADIO_OPEN_GENERAL_EXPORT_LICENCE_ID).click()

    def enter_name(self, name):
        self.driver.find_element_by_id(self.INPUT_NAME_ID).send_keys(name)

    def enter_description(self, description):
        self.driver.find_element_by_id(self.INPUT_DESCRIPTION_ID).send_keys(description)

    def enter_link(self, link):
        self.driver.find_element_by_id(self.INPUT_LINK_ID).send_keys(link)

    def select_registration_required_yes(self):
        self.driver.find_element_by_id(self.RADIO_REGISTRATION_REQUIRED_YES_ID).click()

    def click_controlled_radioactive_tree(self):
        self.driver.find_element_by_id(self.TREE_CONTROLLED_RADIOACTIVE_ID).click()

    def click_united_kingdom_checkbox(self):
        self.driver.find_element_by_id(self.CHECKBOX_UNITED_KINGDOM_ID).click()


class OpenGeneralLicencesEditPage(BasePage):
    pass


class OpenGeneralLicencesDeactivatePage(BasePage):
    pass
