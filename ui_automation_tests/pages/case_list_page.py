import time

import shared.tools.helpers as utils
from shared.BasePage import BasePage
from pages.shared import Shared


class CaseListPage(BasePage):

    # Table
    CASES_TABLE_ROW = ".govuk-table__row"  # CSS
    CASES_TABLE = ".govuk-table"  # CSS
    CHECKBOX_CASE = ".govuk-checkboxes__input[value='"  # CSS
    CHECKBOX_TEXT = ".govuk-checkboxes"  # CSS
    CHECKBOX_SELECT_ALL = "button-select-all"  # ID

    # App Bar Buttons
    BUTTON_ASSIGN_USERS = "assign-users-button"  # ID

    # Filters
    BUTTON_APPLY_FILTERS = "button-apply-filters"  # ID
    BUTTON_CLEAR_FILTERS = "button-clear-filters"  # ID
    LINK_SHOW_FILTERS = "show-filters-link"  # ID
    LINK_HIDE_FILTERS = "hide-filters-link"  # ID
    FILTER_BAR = "lite-filter-bar"  # Class
    STATUS_DROPDOWN = "status"  # ID
    CASE_TYPE_DROPDOWN = "case_type"  # ID

    # Deprecated
    FILTER_SEARCH_BOX = "filter-box"  # ID
    assignee = "[style='margin-bottom: 6px;']"  # CSS
    no_assignee = "[style='margin-bottom: 0; opacity: .7;']"  # CSS

    # Queue dropdown
    queue_dropdown_title = "queue-title"  # ID
    dropdown_item = ".app-dropdown__item"  # CSS
    dropdown_item_class = "app-dropdown__item"  # Class_Name

    # Sort headings
    sort_status = "sort-status"  # ID
    chevron = "chevron"  # ID

    def search_pages_for_id(self, id):
        is_present = len(self.driver.find_elements_by_link_text(id))
        number_of_pages = len(self.driver.find_elements_by_css_selector(".lite-pagination__item"))
        page_number = number_of_pages
        if number_of_pages != 0:
            while is_present == 0:
                url = self.driver.current_url
                if "page" not in url:
                    self.driver.find_element_by_id("page-" + str(number_of_pages)).click()
                else:
                    next_page = url + "&page=" + str(page_number)
                    self.driver.get(next_page)
                page_number -= 1
                is_present = len(self.driver.find_elements_by_link_text(id))

    def click_on_case_checkbox(self, case_id):
        self.driver.set_timeout_to(1)
        self.search_pages_for_id(case_id)
        self.driver.set_timeout_to_10_seconds()
        self.driver.find_element_by_css_selector(self.CHECKBOX_CASE + case_id + "']").click()

    def click_on_assign_users_button(self):
        self.driver.find_element_by_id(self.BUTTON_ASSIGN_USERS).click()

    def get_text_of_assignees(self, driver, case_id):
        self.driver.set_timeout_to(1)
        self.search_pages_for_id(case_id)
        self.driver.set_timeout_to_10_seconds()
        elements = Shared(driver).get_rows_in_lite_table()
        no = utils.get_element_index_by_text(elements, case_id)
        return elements[no].text

    def click_select_all_checkbox(self):
        self.driver.find_element_by_id(self.CHECKBOX_SELECT_ALL).click()

    def get_class_name_of_assign_users_button(self):
        return self.driver.find_element_by_id(self.BUTTON_ASSIGN_USERS).get_attribute("class")

    def enter_name_to_filter_search_box(self, name):
        return self.driver.find_element_by_id(self.FILTER_SEARCH_BOX).send_keys(name)

    def get_text_checkbox_elements(self):
        return self.driver.find_elements_by_css_selector(self.CHECKBOX_TEXT)

    def assert_case_is_present(self, case_id):
        elements = self.driver.find_elements_by_css_selector(self.CASES_TABLE_ROW)
        no = utils.get_element_index_by_text(elements, case_id, complete_match=False)
        return elements[no].is_displayed()

    def click_apply_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_APPLY_FILTERS).click()

    def click_clear_filters_button(self):
        self.driver.find_element_by_id(self.BUTTON_CLEAR_FILTERS).click()

    def click_show_filters_link(self):
        self.driver.find_element_by_id(self.LINK_SHOW_FILTERS).click()

    def click_hide_filters_link(self):
        self.driver.find_element_by_id(self.LINK_HIDE_FILTERS).click()

    def is_filters_visible(self):
        return self.driver.find_element_by_class_name(self.FILTER_BAR).is_displayed()

    def click_on_href_within_cases_table(self, href):
        self.driver.find_element_by_css_selector(self.CASES_TABLE + ' [href*="' + href + '"]').click()

    def click_on_queue_title(self):
        self.driver.find_element_by_id(self.queue_dropdown_title).click()

    def click_chevron_based_on_context_case_id(self, context):
        elements = Shared(self.driver).get_rows_in_lite_table()
        no = utils.get_element_index_by_text(elements, context.case_id)
        elements[no].find_element_by_css_selector(self.chevron).click()

    def click_on_queue_name(self, queue_name):
        self.click_on_queue_title()
        time.sleep(0.5)
        utils.scroll_to_element_by_id(self.driver, queue_name)
        self.driver.find_element_by_id(queue_name).click()

    def select_filter_status_from_dropdown(self, status):
        utils.select_visible_text_from_dropdown(self.driver.find_element_by_id(self.STATUS_DROPDOWN), status)

    def select_filter_case_type_from_dropdown(self, status):
        utils.select_visible_text_from_dropdown(self.driver.find_element_by_id(self.CASE_TYPE_DROPDOWN), status)

    def sort_by_status(self):
        self.driver.find_element_by_id(self.sort_status).click()

    def get_chevron_id_selector(self):
        return self.chevron
