import uuid

from pytest_bdd import scenarios, when, then, given, parsers

from pages.application_page import ApplicationPage
from pages.letter_templates import LetterTemplates
from pages.shared import Shared
from ui_automation_tests.fixtures.add_a_document_template import get_paragraph_text

scenarios("../features/letter_templates.feature", strict_gherkin=False)


@then("my picklist is in template")
def picklist_in_template(driver, context):
    assert context.picklist_text in LetterTemplates(driver).get_text_in_template()


@then("I see my template in the table")
def templates_in_table(driver, context):
    Shared(driver).filter_by_name(context.template_name)
    assert context.template_name in LetterTemplates(driver).get_template_table_text()


@then("I see the drag and drop page")
def see_drag_and_drop_page(driver, context):
    letter_template = LetterTemplates(driver)
    assert context.letter_paragraph_name in letter_template.get_paragraph_drag_and_drop_list_text()
    context.picklist_text = letter_template.get_paragraph_drag_and_drop_list_paragraph_text()


@given("I create a document template")
def create_a_document_template(add_a_document_template):
    pass


@when("I click on my template")
def click_on_my_template(driver, context):
    LetterTemplates(driver).click_letter_template(context.document_template_name)


@then("The template details are present")
def template_details_are_present(driver, context):
    letter_template = LetterTemplates(driver)
    assert context.document_template_name == letter_template.get_template_title()
    assert context.document_template_layout == letter_template.get_template_layout()

    for case_type in context.document_template_case_types:
        assert case_type["reference"]["key"].upper() in letter_template.get_template_case_types()


@then("The paragraph text is present")
def paragraph_text_is_present(driver, context):
    letter_paragraphs = LetterTemplates(driver).get_template_paragraphs()
    for paragraph in context.document_template_paragraph_text:
        assert paragraph in letter_paragraphs


@when("I edit my template name and layout")
def edit_template_name_and_layout(driver, context):
    context.document_template_name = str(uuid.uuid4())[:35]
    letter_template = LetterTemplates(driver)
    letter_template.click_edit_template_button()
    letter_template.enter_template_name(context.document_template_name)
    letter_template.select_which_type_of_cases_template_can_apply_to(["MOD-F680-Clearance"])
    Shared(driver).click_submit()


@when("I edit my template paragraphs")
def edit_template_paragraphs(driver, context, api_test_client):
    letter_template = LetterTemplates(driver)
    letter_template.click_edit_paragraphs_button()
    letter_template.click_add_paragraph_link()
    paragraph_id = letter_template.get_add_paragraph_button()
    context.document_template_paragraph_text.append(get_paragraph_text(api_test_client, paragraph_id))
    Shared(driver).click_submit()


@then("The template paragraphs have been edited")
def template_paragraphs_have_been_edited(driver, context):
    paragraphs_text_list = LetterTemplates(driver).get_paragraph_drag_and_drop_list_paragraph_text()
    for text in context.document_template_paragraph_text:
        assert text in paragraphs_text_list


@then(parsers.parse('"{expected_text}" is shown as position "{no}" in the audit trail'))
def latest_audit_trail(driver, expected_text, no):
    assert expected_text in ApplicationPage(driver).get_text_of_audit_trail_item(int(no) - 1)


@when("I go to letters")
def i_go_to_letters(driver, internal_url):
    driver.get(internal_url.rstrip("/") + "/document-templates")


@when("I click done")
def click_done(driver):
    LetterTemplates(driver).click_done_button()
