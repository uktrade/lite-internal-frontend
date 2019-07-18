import os

from pytest_bdd import when, then, scenarios

from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.attach_document_page import AttachDocumentPage
from ui_automation_tests.pages.documents_page import DocumentsPage

scenarios('../features/document_upload.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I click on the Documents button')
def click_documents(driver):
    application_page = ApplicationPage(driver)
    application_page.click_documents_button()

@when('I click on the Attach Document button')
def click_attach_documents(driver):
    documents_page = DocumentsPage(driver)
    documents_page.click_attach_documents()

@when('I upload file "{filename}" with description "{description}"')
def upload_a_file(driver, filename, description):
    attach_document_page = AttachDocumentPage(driver)

    # Path gymnastics to get the absolute path for $PWD/../resources/(file_to_upload_x) that works everywhere
    file_to_upload_abs_path = \
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'resources', filename))

    attach_document_page.choose_file(file_to_upload_abs_path)
    attach_document_page.enter_description(description)
    attach_document_page.click_submit_btn()

@then('the files are listed on the Documents page newest first')
def check_files_are_uploaded(driver):
    documents_page = DocumentsPage(driver)
    assert documents_page.get_latest_file_name() == file_to_upload_2
    assert documents_page.get_second_latest_file_name() == file_to_upload_1
    assert documents_page.get_latest_file_description() == description_2
    assert documents_page.get_second_latest_file_description() == description_1

