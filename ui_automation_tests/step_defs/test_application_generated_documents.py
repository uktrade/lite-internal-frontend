from faker import Faker
from pytest_bdd import scenarios, when, given, then, parsers

from ui_automation_tests.pages.case_page import CasePage, CaseTabs
from ui_automation_tests.pages.application_page import ApplicationPage
from ui_automation_tests.pages.generate_document_page import GeneratedDocument
from ui_automation_tests.shared import functions
from ui_automation_tests.shared.functions import element_with_id_exists

scenarios("../features/generated_documents.feature", strict_gherkin=False)


@given("I create a template")
def create_template(add_a_document_template):
    pass


@when("I click on the Generate document button")
def click_generated_documents(driver, context):
    CasePage(driver).change_tab(CaseTabs.DOCUMENTS)
    ApplicationPage(driver).click_generate_document_button()


@when(parsers.parse('I add my custom text "{custom_text}"'))
def add_custom_text(driver, context, custom_text):
    GeneratedDocument(driver).add_text_to_edit_text(custom_text)


@when("I click regenerate")
def click_regenerate(driver, context):
    GeneratedDocument(driver).click_regenerate_button()


@then("I see the template text to edit")
def template_text(driver, context):
    text = GeneratedDocument(driver).get_document_text_in_edit_text_area()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in text
        # Remove matched strings to ensure the same string isn't matched twice
        text = text.replace(paragraph, "", 1)


@then("I see the generated document preview")
def generated_document_preview(driver, context):
    generated_document_page = GeneratedDocument(driver)
    assert generated_document_page.preview_is_shown()
    paragraphs = generated_document_page.get_document_paragraph_text_in_preview()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in paragraphs
        # Remove matched strings to ensure the same string isn't matched twice
        paragraphs = paragraphs.replace(paragraph, "", 1)


@then("I see my generated document")
def generated_document(driver, context):
    latest_document = GeneratedDocument(driver).get_latest_document()

    assert context.document_template_name in latest_document.text
    assert "Generated" in latest_document.text
    assert GeneratedDocument(driver).check_download_link_is_present(latest_document)


@then("I see both my generated documents")
def both_generated_documents(driver, context):
    documents = GeneratedDocument(driver).get_documents()

    for document in [documents[0], documents[1]]:
        assert context.document_template_name in document.text
        assert "Generated" in document.text
        assert GeneratedDocument(driver).check_download_link_is_present(document)

    # Check 2 documents have been created
    assert documents[0].text != documents[1].text


@when("I leave the default addressee")
def default_addressee(driver):
    if element_with_id_exists(driver, "addressee-applicant"):
        functions.click_submit(driver)


@given("I create an additional contact for the case")
def create_additional_contact(context, api_test_client):
    fake = Faker()
    contact = api_test_client.parties.add_additional_contact(
        context.app_id,
        {
            "name": fake.name(),
            "email": fake.free_email(),
            "phone_number": fake.phone_number(),
            "details": fake.prefix(),
            "address": fake.address(),
            "country": "GB",
            "type": "additional_contact",
        },
    )
    context.contact_id = contact["id"]
    context.contact_name = contact["name"]
    context.contact_email = contact["email"]


@when("I select the addressee previously created")
def select_addressee(context, driver):
    GeneratedDocument(driver).select_addressee(context.contact_id)
    functions.click_submit(driver)


@then("I see the addressee in the document")
def addressee_in_preview(driver, context):
    text = GeneratedDocument(driver).get_document_preview_text()
    assert context.contact_name in text
    assert context.contact_email in text
