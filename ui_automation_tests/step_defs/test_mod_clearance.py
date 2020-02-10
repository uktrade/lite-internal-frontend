from pytest_bdd import scenarios, when, then, given

from pages.application_page import ApplicationPage

scenarios("../features/mod_clearance.feature", strict_gherkin=False)


@given("an Exhibition Clearance is created")  # noqa
def an_exhibition_clearance_is_created(driver, apply_for_exhibition_clearance):
    pass


@given("an F680 Clearance is created")  # noqa
def an_f680_clearance_is_created(driver, apply_for_f680_clearance):
    pass


@given("an Gifting Clearance is created")  # noqa
def an_gifting_clearance_is_created(driver, apply_for_gifting_clearance):
    pass


@when("I click on the MOD Clearance case")  # noqa
def i_click_on_the_exhibition_clearance_case(driver, context):
    driver.find_element_by_link_text(context.reference_code).click()


@then("I see the MOD Clearance case page")  # noqa
def i_see_the_exhibition_clearance_case_page(driver, context):
    assert driver.find_element_by_id(ApplicationPage.HEADING_ID).text == context.reference_code
