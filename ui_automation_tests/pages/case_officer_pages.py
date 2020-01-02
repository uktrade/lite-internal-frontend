from shared.BasePage import BasePage


class CaseOfficerPages(BasePage):
    ASSIGN_BTN = "assign"  # id
    UNASSIGN_BTN = "unassign"  # id
    CHOICES = ".govuk-radios__item"  # css
    CHOICES_NAMES = ".govuk-radios__item label"
    CURRENT_CASE_OFFICER_PANEL = ".app-case-board"
    SEARCH_TXT = "search"  # id
    SEARCH_BTN = ".lite-search__button"  # css
    RADIO_BUTTON = "input[name='user']"

    def select_first_user(self):
        self.driver.find_elements_by_css_selector(self.RADIO_BUTTON)[0].click()

    def click_assign(self):
        self.driver.find_element_by_id(self.ASSIGN_BTN).click()

    def click_unassign(self):
        self.driver.find_element_by_id(self.UNASSIGN_BTN).click()

    def search(self, text):
        self.driver.find_element_by_id(self.SEARCH_TXT).send_keys(text)
        self.driver.find_element_by_css_selector(self.SEARCH_BTN).click()

    def get_users_name(self):
        return self.driver.find_elements_by_css_selector(self.CHOICES_NAMES)

    def is_current_case_officer(self):
        # returns 0 or 1 depending on if element exists
        return len(self.driver.find_elements_by_css_selector(self.CURRENT_CASE_OFFICER_PANEL))
