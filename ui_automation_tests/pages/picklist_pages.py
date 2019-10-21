class PicklistPages():

    def __init__(self, driver):
        self.driver = driver
        self.picklist_tab = '.lite-tabs__tab[href*="picklists"]' #css
        self.picklist_edit_button = '.govuk-button[href*="edit"]' #css
        self.picklist_add_button = '.govuk-button[href*="add"]' #css
        self.picklist_deactivate_button = '.govuk-button[href*="deactivate"]' #css
        self.picklist_reactivate_button = '.govuk-button[href*="reactivate"]' #css
        self.picklist_type_sub_nav = '.govuk-link[href*="type=' #css
        self.picklist_page_body = '.govuk-main-wrapper' #css
        self.picklist_name_field = 'name' #name
        self.picklist_description_field = 'text' #name
        self.picklist_names_in_list = 'h4 a' #css
        self.picklist_list_name = '.govuk-heading-s' #css
        self.picklist_list_description = '.app-picklist-item__text' #css

        self.context_suggestions_overlay = 'context_suggestion'  # ID

    def click_on_picklist_tab(self):
        self.driver.find_element_by_css_selector(self.picklist_tab).click()

    def click_on_picklist_edit_button(self):
        self.driver.find_element_by_css_selector(self.picklist_edit_button).click()

    def click_on_picklist_deactivate_button(self):
        self.driver.find_element_by_css_selector(self.picklist_deactivate_button).click()

    def click_on_picklist_reactivate_button(self):
        self.driver.find_element_by_css_selector(self.picklist_reactivate_button).click()

    def click_on_picklist_type_sub_nav(self, type):
        self.driver.find_element_by_css_selector(self.picklist_type_sub_nav + type + '"]').click()

    def click_on_picklist_add_button(self):
        self.driver.find_element_by_css_selector(self.picklist_add_button).click()

    def get_text_of_picklist_page_body(self):
        return self.driver.find_element_by_css_selector(self.picklist_page_body).text

    def get_latest_picklist_name(self):
        return self.driver.find_elements_by_css_selector(self.picklist_list_name)[-1].text

    def get_latest_picklist_description(self):
        return self.driver.find_elements_by_css_selector(self.picklist_list_description)[-1].text

    def type_into_picklist_name(self, name):
        self.driver.find_element_by_name(self.picklist_name_field).send_keys(name)

    def type_into_picklist_description(self, description):
        self.driver.find_element_by_name(self.picklist_description_field).send_keys(description)

    def get_elements_of_picklist_names_in_list(self):
        return self.driver.find_elements_by_css_selector(self.picklist_names_in_list)

    def context_suggestions_are_displayed(self):
        return self.driver.find_element_by_id(self.context_suggestions_overlay).is_displayed()

    def get_context_suggestion_variable_name(self):
        return self.driver.find_element_by_id(self.context_suggestions_overlay).text.split(" ")[0]

    def click_context_suggestion(self):
        self.driver.find_element_by_id(self.context_suggestions_overlay).click()
