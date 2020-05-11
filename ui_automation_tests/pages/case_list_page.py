import time

import shared.tools.helpers as utils
from selenium.webdriver.support.select import Select
from shared.BasePage import BasePage
from pages.shared import Shared


class CaseListPage(BasePage):

    # Table
    CASES_TABLE_ROW = ".govuk-table__row"  # CSS
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
    USER_STATUS_DROPDOWN_ID = "status"
    STATUS_DROPDOWN = "status"  # ID
    CASE_TYPE_DROPDOWN = "case_type"  # ID
    INPUT_ASSIGNED_USER_ID = "assigned_user"
    FILTER_SEARCH_BOX = "filter-box"  # ID
    SHOW_TEAM_ECJU = "Show cases with open enquiries by your team"
    QUEUE_SEARCH_BOX = "filter-queues"
    # Queue dropdown
    LINK_CHANGE_QUEUE_ID = "link-queue"

    # Sort headings
    SORT_STATUS = "sort-status"  # ID

    # Notification for updated cases
    EXPORTER_AMENDMENTS_BANNER = "exporter-amendments-banner"  # ID

    # SLA
    SLA_ID = "sla"

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

    def click_on_queue_title(self):
        self.driver.find_element_by_id(self.LINK_CHANGE_QUEUE_ID).click()

    def search_for_queue(self, queue_name):
        self.driver.find_element_by_id(self.QUEUE_SEARCH_BOX).send_keys(queue_name)

    def click_on_queue_name(self, queue_name):
        self.click_on_queue_title()
        time.sleep(0.5)
        self.search_for_queue(queue_name)
        self.driver.find_element_by_id(queue_name).click()

    def select_filter_status_from_dropdown(self, status):
        Select(self.driver.find_element_by_id(self.STATUS_DROPDOWN)).select_by_visible_text(status)

    def select_filter_user_status_from_dropdown(self, status):
        Select(self.driver.find_element_by_id(self.USER_STATUS_DROPDOWN_ID)).select_by_visible_text(status)

    def select_filter_case_type_from_dropdown(self, status):
        Select(self.driver.find_element_by_id(self.CASE_TYPE_DROPDOWN)).select_by_visible_text(status)

    def sort_by_status(self):
        self.driver.find_element_by_id(self.SORT_STATUS).click()

    def click_on_exporter_amendments_banner(self):
        self.driver.find_element_by_id(self.EXPORTER_AMENDMENTS_BANNER).click()

    def enter_assigned_user_filter_text(self, text):
        self.driver.find_element_by_id(self.INPUT_ASSIGNED_USER_ID).send_keys(text)

    def enter_name_to_filter_search_box(self, text):
        self.driver.find_element_by_id(self.FILTER_SEARCH_BOX).send_keys(text)

    def get_case_row(self, case_id):
        return self.driver.find_element_by_id(case_id)

    def get_case_row_sla(self, row):
        return row.find_element_by_id(self.SLA_ID).text

    def click_checkbox_to_show_team_ecju_query(self):
        return self.driver.find_element_by_id(self.SHOW_TEAM_ECJU).click()
