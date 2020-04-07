from pytest_bdd import then, scenarios, given, when
from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/eua_queries.feature", strict_gherkin=False)


@given("I create eua query or eua query has been previously created")  # noqa
def create_eua(driver, apply_for_eua_query):
    pass


@then("I should see the ability to add case notes")
def case_notes_are_available(driver):
    assert driver.find_element_by_id(ApplicationPage.INPUT_CASE_NOTE_ID)


@then("The dropdown should contain Move Case, Documents, and Ecju queries")
def dropdown_contains_correct_functionality(driver):
    application_page = ApplicationPage(driver)
    application_page.click_drop_down()
    assert application_page.get_document_element()
    assert application_page.get_move_case_element()
    assert application_page.get_ecju_queries_element()
    assert application_page.is_change_status_available()
    assert application_page.get_case_officer_element()
    assert application_page.get_generate_document_element()
    assert application_page.get_assign_user_element()
    assert application_page.get_additional_contacts_element()


@then("the status has been changed in the end user advisory")
def check_status_has_changed(driver):
    assert "closed" in ApplicationPage(driver).get_text_of_case_note_subject(0)


@when("I go to end user advisory previously created")  # noqa
def click_on_created_eua(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.eua_id)
