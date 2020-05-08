from pytest_bdd import then, scenarios, given, when

from pages.case_page import CasePage, CaseTabs
from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/eua_queries.feature", strict_gherkin=False)


@given("I create eua query or eua query has been previously created")  # noqa
def create_eua(driver, apply_for_eua_query):
    pass


@then("I should see the ability to add case notes")
def case_notes_are_available(driver):
    assert driver.find_element_by_id(ApplicationPage.INPUT_CASE_NOTE_ID)


@then("the status has been changed in the end user advisory")
def check_status_has_changed(driver):
    case_page = CasePage(driver)
    case_page.change_tab(CaseTabs.ACTIVITY)
    assert "closed" in case_page.get_audit_trail_text().lower()


@when("I go to end user advisory previously created")  # noqa
def click_on_created_eua(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.eua_id)
