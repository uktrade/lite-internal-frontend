from pytest_bdd import then, scenarios

from ui_automation_tests.pages.application_page import ApplicationPage

scenarios("../features/view_open_application.feature", strict_gherkin=False)


@then("I see the Open Application case page")  # noqa
def i_see_the_open_application_case_page(driver, context):
    assert driver.find_element_by_id(ApplicationPage.HEADING_ID).text == context.reference_code
