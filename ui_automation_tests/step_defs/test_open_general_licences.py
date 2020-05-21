from pytest_bdd import scenarios, when, then

from pages.open_general_licences_pages import OpenGeneralLicencesListPage, OpenGeneralLicencesCreatePage, \
    OpenGeneralLicencesDetailPage
from shared import functions
from faker import Faker

scenarios("../features/open_general_licences.feature", strict_gherkin=False)


fake = Faker()


@when("I go to open general licences")
def go_to_open_general_licences(driver, internal_url):
    driver.get(internal_url.rstrip("/") + "/open-general-licences/")


@when("I click the new open general licence button")
def click_the_open_general_licence_button(driver):
    OpenGeneralLicencesListPage(driver).click_new_open_general_licence_button()


@when("I select Open General Export Licence")
def select_open_general_export_licence(driver):
    OpenGeneralLicencesCreatePage(driver).select_open_general_export_licence_radiobutton()
    functions.click_submit(driver)


@when("I fill in details about the licence")
def fill_in_details(driver, context):
    context.ogl_name = fake.bs()
    context.ogl_description = fake.bs()
    context.ogl_link = "https://www.gov.uk/government/publications/open-general-export-licence-military-" \
                       "goods-government-or-nato-end-use--6"

    create_page = OpenGeneralLicencesCreatePage(driver)
    create_page.enter_name(context.ogl_name)
    create_page.enter_description(context.ogl_description)
    create_page.enter_link(context.ogl_link)
    create_page.select_registration_required_yes()
    functions.click_submit(driver)


@when("I select the tree Controlled Radioactive Sources")
def select_control_list_entry(driver):
    OpenGeneralLicencesCreatePage(driver).click_controlled_radioactive_tree()
    functions.click_submit(driver)


@when("I select the country United Kingdom")
def select_united_kingdom(driver):
    OpenGeneralLicencesCreatePage(driver).click_united_kingdom_checkbox()
    functions.click_submit(driver)


@then("I see the summary list")
def see_the_summary_list(driver):
    pass


@when("I click submit")
def click_submit(driver):
    functions.click_submit(driver, button_value="finish")


@then("I see the newly generated open general export licence")
def see_the_newly_generated_open_general_export_licence(driver, context):
    open_general_licences_list_page = OpenGeneralLicencesListPage(driver)
    open_general_licences_list_page.filter_by_name(context.ogl_name)
    open_general_licences_list_page.click_view_first_ogl_link()

    summary_list_text = OpenGeneralLicencesDetailPage(driver).get_summary_list_text()
    assert context.ogl_name in summary_list_text
    assert context.ogl_description in summary_list_text
    assert context.ogl_link in summary_list_text
    assert "Yes" in summary_list_text
    assert "Controlled Radioactive Sources" in summary_list_text
    assert "United Kingdom" in summary_list_text
