from pytest_bdd import when, then, scenarios
from ui_automation_tests.pages.case_list_page import CaseListPage
from ui_automation_tests.pages.application_page import ApplicationPage

scenarios('../features/end_user_advisory_query.feature', strict_gherkin=False)


@when('I go to eua query previously created')
def click_on_created_application(driver):
    caselistpage = CaseListPage(driver)
    caselistpage.click_show_filters_link()
    caselistpage.select_filter_case_type_from_dropdown("End User Advisory Query")
    caselistpage.click_apply_filters_button()
    caselistpage.click_on_case_by_num(0)


@then('I should see flags can be added')
def flags_are_available(driver):
    flags = 'application-edit-case-flags'  # id
    application_page = ApplicationPage(driver)
    assert application_page.is_flag_available()


@then('I should see the ability to add case notes')
def case_notes_are_available(driver):
    case_notes = 'case_note'
    assert driver.find_element_by_id(case_notes)


@then('The dropdown should contain Move Case, Documents, and Ecju queries')
def dropdown_contains_correct_functionality(driver):
    application_page = ApplicationPage(driver)
    application_page.click_drop_down()
    assert application_page.is_document_available()
    assert application_page.is_move_case_available()
    assert application_page.is_ecju_queries_available()
    assert application_page.is_change_status_available()
    assert len(driver.find_elements_by_xpath('//div[@class="lite-app-bar__controls"]//div//a')) == 4
