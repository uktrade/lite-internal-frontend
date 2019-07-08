class AddGoodPage:

    def __init__(self, driver):
        self.driver = driver
        self.add_a_good_btn = "#add-a-good"
        self.goods_edit_link = "[href*='goods/edit']"
        self.goods_delete_link = "[href*='goods/delete']"
        self.goods_delete_button = ".govuk-button--warning"
        self.description_xpath_prefix = "//*[text()[contains(.,'%s')]]"
        self.clc_query_case_id_xpath_prefix = "%s/../*[@data_good_clc_query_case_id]"

    def click_add_a_good(self):
        self.driver.find_element_by_css_selector(self.add_a_good_btn).click()

    def enter_description_of_goods(self, description):
        description_tb = self.driver.find_element_by_id("description")
        description_tb.clear()
        description_tb.send_keys(description)

    def select_is_your_good_controlled(self):
        self.driver.find_element_by_id("is_good_controlled-unsure").click()

    def enter_control_unsure_details(self, details):
        unsure_details = self.driver.find_element_by_id("not_sure_details_details")
        unsure_details.clear()
        unsure_details.send_keys(details)

    def select_control_unsure_confirmation(self):
        self.driver.find_element_by_id("clc_query_confirmation-yes").click()

    def select_is_your_good_intended_to_be_incorporated_into_an_end_product(self):
        self.driver.find_element_by_id("is_good_end_product-no").click()

    def assert_good_is_displayed_and_return_case_id(self, description):
        description_xpath = self.description_xpath_prefix % description
        clc_query_case_id_xpath = self.clc_query_case_id_xpath_prefix % description_xpath

        goods_row = self.driver.find_element_by_xpath(description_xpath)
        clc_query_case_id = self.driver.find_element_by_xpath(clc_query_case_id_xpath).get_attribute("data_good_clc_query_case_id")

        assert goods_row.is_displayed()

        return clc_query_case_id
