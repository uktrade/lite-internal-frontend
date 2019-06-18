from datetime import datetime

import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.organisations_form_page import OrganisationsFormPage
from pages.organisations_page import OrganisationsPage
from pages.register_a_business_page import RegisterABusinessPage
from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.common.by import By

scenarios('../features/organisation_setup.feature')


@when('I register a new organisation')
def register_organisation(driver):
    internal_hub = RegisterABusinessPage(driver)

    internal_hub.click_manage_organisations_link()

    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Test Org')]]")
    if not exists:
        # New Organisation
        internal_hub.click_new_organisation()

        internal_hub.enter_business_name("Test Org")
        internal_hub.enter_eori_number("GB987654312000")
        internal_hub.enter_sic_number("73200")
        internal_hub.enter_vat_number("123456789")
        internal_hub.enter_company_registration_number("000000011")
        internal_hub.click_save_and_continue()

        internal_hub.enter_site_name("Site 1")
        internal_hub.enter_address_line_1("123 Cobalt Street")
        internal_hub.enter_address_line_2("123 Cobalt Street")
        internal_hub.enter_zip_code("N23 6YL")
        internal_hub.enter_city("London")
        internal_hub.enter_state("London")
        internal_hub.enter_country("Ukraine")

        internal_hub.click_save_and_continue()

        internal_hub.enter_email("test@mail.com")
        internal_hub.enter_first_name("Test")
        internal_hub.enter_last_name("User1")
        internal_hub.enter_password("password")

        internal_hub.click_submit()


@then('organisation is registered')
def verify_registered_organisation(driver):
    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Unicorns Ltd')]]")
    assert exists


@when('I go to organisations')
def i_go_to_organisations(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_organisations()


@when('I choose to add a new organisation')
def i_choose_to_add_a_new_organisation(driver):
    organisations_page = OrganisationsPage(driver)
    organisations_page.click_new_organisation_btn()


@when(parsers.parse('I provide company registration details of name: "{name}", EORI: "{eori}", SIC: "{sic}", VAT: "{vat}", CRN: "{registration}"'))
def fill_out_company_details_page_and_continue(driver, name, eori, sic, vat, registration):
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_name(name)
    organisations_form_page.enter_eori_number(eori)
    organisations_form_page.enter_sic_number(sic)
    organisations_form_page.enter_vat_number(vat)
    organisations_form_page.enter_registration_number(registration)
    organisations_form_page.click_submit()


@when(parsers.parse('I setup an intial site with name: "{name}", addres line 1: "{address_line_1}", town or city: "{city}", County: "{region}", post code: "{post_code}", country: "{country}"'))
def fill_out_site_details(driver, name, address_line_1, city, region, post_code, country):
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_site_name(name)
    organisations_form_page.enter_address_line_1(address_line_1)
    organisations_form_page.enter_region(region)
    organisations_form_page.enter_post_code(post_code)
    organisations_form_page.enter_city(city)
    organisations_form_page.enter_country(country)
    organisations_form_page.click_submit()


@when(parsers.parse('I setup the admin user with email: "{email}", first name: "{first_name}", last name: "{last_name}", password: "{password}"'))
def fill_out_admin_user_details(driver, email, first_name, last_name, password):
    organisations_form_page = OrganisationsFormPage(driver)
    organisations_form_page.enter_email(datetime.now().strftime("%m%d%H%M") + email)
    organisations_form_page.enter_first_name(first_name)
    organisations_form_page.enter_last_name(last_name)
    organisations_form_page.enter_password(password)
    organisations_form_page.click_submit()
