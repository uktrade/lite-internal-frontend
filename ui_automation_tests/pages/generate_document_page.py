from ui_automation_tests.shared.BasePage import BasePage


class GeneratedDocument(BasePage):
    PREVIEW = "preview"  # ID
    PARAGRAPHS = "paragraph_content"  # ID
    DOWNLOAD = "link-download"  # ID
    TEXT = "text"  # ID
    ADD_PARAGRAPHS = "add_paragraphs"  # name
    PARAGRAPH_CHECKBOXES = "text[]"  # name

    def click_letter_template(self, document_template_name):
        self.driver.find_element_by_id(document_template_name).click()

    def preview_is_shown(self):
        return self.driver.find_element_by_id(self.PREVIEW).is_displayed()

    def get_document_text_in_preview(self):
        return self.driver.find_element_by_id(self.PARAGRAPHS).text

    def check_download_link_is_present(self, row):
        return row.find_element_by_id(self.DOWNLOAD).is_displayed()

    def get_document_text_in_edit(self):
        return self.driver.find_element_by_id(self.TEXT).text

    def click_add_paragraphs_link(self):
        self.driver.find_element_by_name(self.ADD_PARAGRAPHS).click()

    def uncheck_all_paragraphs_except_last(self):
        checkboxes = self.driver.find_elements_by_name(self.PARAGRAPH_CHECKBOXES)
        for i in range(len(checkboxes) - 1):
            if checkboxes[i].is_selected():
                checkboxes[i].click()

        if not checkboxes[-1].is_selected():
            checkboxes[-1].click()
        return checkboxes[-1].get_attribute("value")

    def add_text_to_edit_text(self, text):
        return self.driver.find_element_by_id(self.TEXT).send_keys(text)
