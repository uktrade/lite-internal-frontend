from pytest_bdd import scenarios, when, then

from pages.organisation_page import OrganisationPage
from pages.organisations_form_page import OrganisationsFormPage
from pages.organisations_page import OrganisationsPage
from pages.shared import Shared
from shared import functions
from shared.tools.wait import wait_until_page_is_loaded
from faker import Faker

scenarios("../features/organisation.feature", strict_gherkin=False)

fake = Faker()


@then("commercial organisation is registered")
def verify_registered_organisation(driver, context):
    wait_until_page_is_loaded(driver)
    # Assert that the success info bar is visible
    assert functions.element_with_css_selector_exists(driver, ".lite-info-bar")
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    row = OrganisationPage(driver).get_organisation_row()
    assert context.organisation_name in row["name"]
    assert context.eori in row["eori-number"]
    assert context.sic in row["sic-number"]
    assert context.vat in row["vat-number"]


@then("organisation is edited")
def verify_edited_organisation(driver, context):
    wait_until_page_is_loaded(driver)
    # Assert that the success info bar is visible
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    row = OrganisationPage(driver).get_organisation_row()
    assert context.organisation_name in row["name"]
    assert context.eori in row["eori-number"]
    assert context.sic in row["sic-number"]
    assert context.vat in row["vat-number"]


@then("individual organisation is registered")
def verify_registered_individual_organisation(driver, context):
    wait_until_page_is_loaded(driver)
    # Assert that the success info bar is visible
    assert functions.element_with_css_selector_exists(driver, ".lite-info-bar")
    OrganisationsPage(driver).search_for_org_in_filter(context.organisation_name)
    row = OrganisationPage(driver).get_organisation_row()
    assert context.organisation_name in row["name"]
    assert context.eori in row["eori-number"]


@then("HMRC organisation is registered")
def verify_hmrc_registered_organisation(driver, context):
    OrganisationsPage(driver).search_for_org_in_filter(context.hmrc_org_name)
    assert context.hmrc_org_name in Shared(driver).get_text_of_lite_table_body()


@when("I add a new commercial organisation")
def i_choose_to_add_a_new_commercial_organisation(driver, context):
    OrganisationsPage(driver).click_new_organisation_button()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.select_type("commercial")
    organisations_form_page.select_location("united_kingdom")
    organisations_form_page.fill_in_company_info_page_1(context)
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_site_details(context, "united_kingdom")
    context.email = fake.free_email()
    organisations_form_page.enter_email(context.email)


@when("I add a new individual organisation")
def i_choose_to_add_a_new_individual_organisation(driver, context):
    OrganisationsPage(driver).click_new_organisation_button()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.select_type("individual")
    organisations_form_page.select_location("abroad")
    organisations_form_page.fill_in_individual_info_page_1(context)
    organisations_form_page.enter_site_details(context, "abroad")


@when("I add a new HMRC organisation")
def i_choose_to_add_a_new_hmrc_organisation(driver, context):
    OrganisationsPage(driver).click_new_organisation_button()
    context.hmrc_org_name = fake.company() + " " + fake.company_suffix()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_name(context.hmrc_org_name)
    organisations_form_page.enter_site_details(context, "united_kingdom")
    context.email = fake.free_email()
    organisations_form_page.enter_email(context.email)


@then("the previously created organisations flag is assigned")  # noqa
def assert_flag_is_assigned(driver, context):
    assert OrganisationPage(driver).is_organisation_flag_applied(context.flag_name)


@when("I go to organisations")
def i_go_to_organisations(driver, internal_url, context):
    driver.get(internal_url.rstrip("/") + "/organisations")


@when("I click the organisation")
def click_organisation(driver, context):
    OrganisationsPage(driver).click_organisation(context.organisation_name)


@when("I edit the organisation")
def click_edit(driver, context):
    OrganisationPage(driver).click_edit_organisation()
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.select_type("commercial")
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.fill_in_company_info_page_1(context)
