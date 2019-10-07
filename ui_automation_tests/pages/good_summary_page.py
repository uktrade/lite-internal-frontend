from helpers.BasePage import BasePage


class GoodSummaryPage(BasePage):
    edit_goods_flags = 'button-edit-goods-flags'  # ID
    add_report_summary = 'button-add-report-summary' # ID

    def click_edit_good_flags(self):
        edit_goods_btn = self.driver.find_element_by_id(self.edit_goods_flags)
        edit_goods_btn.click()

    def click_add_report_summary(self):
        return self.driver.find_element_by_id(self.add_report_summary).click()

    def check_control_code(self):
        rows = self.driver.find_elements_by_css_selector('.lite-table__body>.lite-table__row')
        for row in rows:
            assert 'ML4b1' in row.find_elements_by_css_selector('.lite-table__cell')[3].text
