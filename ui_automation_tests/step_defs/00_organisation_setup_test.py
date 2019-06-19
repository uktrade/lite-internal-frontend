from datetime import datetime

import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.organisations_form_page import OrganisationsFormPage
from pages.organisations_page import OrganisationsPage
from pytest_bdd import scenarios, when, then, parsers
from selenium.webdriver.common.by import By
from conftest import context

scenarios('../features/organisation_setup.feature')


@then('organisation is registered')
def verify_registered_organisation(driver):
    if not context.org_registered_status:
        exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'" + context.org_name + "')]]")
        assert exists


@when('I go to organisations')
def i_go_to_organisations(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_organisations()


@when('I choose to add a new organisation')
def i_choose_to_add_a_new_organisation(driver):
    context.org_registered_status = False
    organisations_page = OrganisationsPage(driver)
    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Unicorns Ltd')]]")
    if exists:
        context.org_registered_status = True
    else:
        organisations_page.click_new_organisation_btn()


@when(parsers.parse('I provide company registration details of name: "{name}", EORI: "{eori}", SIC: "{sic}", VAT: "{vat}", CRN: "{registration}"'))
def fill_out_company_details_page_and_continue(driver, name, eori, sic, vat, registration):
    if not context.org_registered_status:
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_name(name)
        context.org_name = name
        organisations_form_page.enter_eori_number(eori)
        organisations_form_page.enter_sic_number(sic)
        organisations_form_page.enter_vat_number(vat)
        organisations_form_page.enter_registration_number(registration)
        organisations_form_page.click_submit()


@when(parsers.parse('I setup an initial site with name: "{name}", addres line 1: "{address_line_1}", town or city: "{city}", County: "{region}", post code: "{post_code}", country: "{country}"'))
def fill_out_site_details(driver, name, address_line_1, city, region, post_code, country):
    if not context.org_registered_status:
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
    if not context.org_registered_status:
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_email(email)
        organisations_form_page.enter_first_name(first_name)
        organisations_form_page.enter_last_name(last_name)
        organisations_form_page.enter_password(password)
        organisations_form_page.click_submit()
