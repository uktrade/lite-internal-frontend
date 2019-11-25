from ui_automation_tests.shared.BasePage import BasePage


class GeneratedDocument(BasePage):
    preview = ".app-letter-preview__page"  # css
    paragraphs = "paragraph_content"  # ID
    download = "download"  # ID

    def click_letter_template(self, document_template_name):
        self.driver.find_element_by_id(document_template_name).click()

    def preview_is_shown(self):
        return self.driver.find_element_by_css_selector(self.preview).is_displayed()

    def get_document_text(self):
        return self.driver.find_element_by_id(self.paragraphs).text

    def check_download_link_is_present(self, row):
        return row.find_element_by_id(self.download).is_displayed()
