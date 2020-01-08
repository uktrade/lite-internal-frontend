from pytest_bdd import then, scenarios, given
from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/eua_queries.feature", strict_gherkin=False)


@given("I create eua query or eua query has been previously created")  # noqa
def create_eua(driver, apply_for_eua_query):
    pass


@then("I should see the ability to add case notes")
def case_notes_are_available(driver):
    case_notes = "case_note"
    assert driver.find_element_by_id(case_notes)


@then("The dropdown should contain Move Case, Documents, and Ecju queries")
def dropdown_contains_correct_functionality(driver):
    application_page = ApplicationPage(driver)
    application_page.click_drop_down()
    assert application_page.get_document_element()
    assert application_page.get_move_case_element()
    assert application_page.get_ecju_queries_element()
    assert application_page.is_change_status_available()
    assert application_page.get_case_officer_element()
    # This tests that the expected elements are the only ones that appear, and that any new functionality added
    # should be tested if not tested elsewhere.
    assert len(driver.find_elements_by_css_selector("div.lite-app-bar__controls>div>a")) == 5


@then("the status has been changed in the end user advisory")
def check_status_has_changed(driver):
    assert "closed" in ApplicationPage(driver).get_text_of_case_note_subject(0)


@then("I should see flags can be added")
def flags_are_available(driver):
    application_page = ApplicationPage(driver)
    assert application_page.get_case_flag_element()
