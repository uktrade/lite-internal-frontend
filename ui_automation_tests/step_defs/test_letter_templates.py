from pytest_bdd import scenarios, when, then, given
import shared.tools.helpers as utils

from pages.header_page import HeaderPage
from pages.letter_templates import LetterTemplates
from pages.shared import Shared

scenarios('../features/letter_templates.feature', strict_gherkin=False)


@given("I create a letter paragraph picklist")
def add_letter_paragraph_picklist(add_a_letter_paragraph_picklist):
    pass


@when('I go to letters')
def go_to_letters(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_letters()


@when("I create a letter template")
def create_letter_template(driver, context):
    LetterTemplates(driver).click_create_a_template()
    context.template_name = 'Template ' + utils.get_formatted_date_time_m_d_h_s()
    LetterTemplates(driver).enter_template_name(context.template_name)
    Shared(driver).click_submit()
    LetterTemplates(driver).select_which_type_of_case_template_can_apply_to('Applications')
    Shared(driver).click_submit()
    LetterTemplates(driver).select_which_type_of_case_template_can_apply_to('layout-licence')
    Shared(driver).click_submit()


@when("I add a letter paragraph to template")
def add_two_letter_paragraphs(driver, context):
    letter_template = LetterTemplates(driver)
    letter_template.click_add_letter_paragraph()
    x = letter_template.add_letter_paragraph()
    letter_template.click_add_letter_paragraphs()


@when("I preview template")
def preview_template(driver):
    LetterTemplates(driver).click_create_preview_button()


@then("my picklist is in template")
def picklist_in_template(driver, context):
    assert context.picklist_text in LetterTemplates(driver).get_text_of_paragraphs_in_template()


@when("I click save")
def click_save(driver):
    LetterTemplates(driver).click_save_button()


@then("I see my template in the table")
def templates_in_table(driver, context):
    assert context.template_name in Shared(driver).get_text_of_table()


@when("I edit my template")
def edit_template(driver, context):
    driver.find_element_by_link_text(context.template_name).click()
    LetterTemplates(driver).click_edit_details_button()
    context.template_name = context.template_name + ' edited'
    LetterTemplates(driver).enter_template_name(context.template_name)
    Shared(driver).click_submit()
    Shared(driver).click_back()


@then("I see the drag and drop page")
def see_drag_and_drop_page(driver, context):
    context.picklist_text = context.api.request_data['letter_paragraph_picklist']['text']
    assert 'app-sortable ui-sortable' in LetterTemplates(driver).get_class_name_of_drag_and_drop_list()
    assert context.letter_paragraph_name in LetterTemplates(driver).get_text_of_paragraphs_in_preview()
