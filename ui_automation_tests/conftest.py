import os
import pytest
import datetime
from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from selenium import webdriver
from pages.flags_pages import FlagsPages
from pages.shared import Shared
from conf.settings import env
from pages.header_page import HeaderPage
from pages.organisations_form_page import OrganisationsFormPage
from pages.organisations_page import OrganisationsPage
from pages.exporter_hub import ExporterHub
from selenium.webdriver.common.by import By
import helpers.helpers as utils

# Screenshot in case of any test failure


def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = "{0}_{1}".format(class_name, exporter_url)
        # utils.save_screenshot(node.funcargs.get("driver"), name)


# Create driver and url command line addoption
def pytest_addoption(parser):
    env = str(os.environ.get('ENVIRONMENT'))
    if env == 'None':
        env = "uat"
    print("touched: " + env)
    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption("--exporter_url", action="store",
                     default="https://exporter.lite.service." + env + ".uktrade.io/", help="url")
    parser.addoption("--internal_url", action="store",
                     default="https://internal.lite.service." + env + ".uktrade.io/", help="url")
    #parser.addoption("--exporter_url", action="store", default="http://localhost:8300", help="url")
    #parser.addoption("--internal_url", action="store", default="http://localhost:8200", help="url")
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


# Create driver fixture that initiates chrome
@pytest.fixture(scope="session", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")
    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver")
        else:
            browser = webdriver.Chrome()
        browser.get("about:blank")
        browser.implicitly_wait(3)
        return browser
    else:
        print('only chrome is supported at the moment')

    def fin():
        driver.quit()
        request.addfinalizer(fin)


@pytest.fixture
def context():
    class Context(object):
        pass

    return Context()


# Create url fixture
@pytest.fixture(scope="module")
def exporter_url(request):
    return request.config.getoption("--exporter_url")


@pytest.fixture(scope="module")
def internal_url(request):
    return request.config.getoption("--internal_url")


@pytest.fixture
def test_teardown(driver):
    driver.quit()


@pytest.fixture(scope="module")
def sso_sign_in_url(request):
    return request.config.getoption("--sso_sign_in_url")


@pytest.fixture(scope="module")
def invalid_username():
    return "invalid@mail.com"


sso_email = env('TEST_SSO_EMAIL')
sso_password = env('TEST_SSO_PASSWORD')


@pytest.fixture(scope="session")
def set_up_org(driver, request):
    driver.get(request.config.getoption("--sso_sign_in_url"))
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(request.config.getoption("--internal_url"))
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_organisations()
    context.org_registered_status = False
    organisations_page = OrganisationsPage(driver)
    exists = utils.is_element_present(driver, By.XPATH, "//*[text()[contains(.,'Unicorns Ltd')]]")
    if exists:
        context.org_registered_status = True
    else:
        organisations_page.click_new_organisation_btn()
    if not context.org_registered_status:
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_name("Unicorns Ltd")
        context.org_name = "Unicorns Ltd"
        organisations_form_page.enter_eori_number("1234567890AAA")
        organisations_form_page.enter_sic_number("2345")
        organisations_form_page.enter_vat_number("GB1234567")
        organisations_form_page.enter_registration_number("09876543")
        organisations_form_page.click_submit()
    if not context.org_registered_status:
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_site_name("Headquarters")
        context.site_name = "Headquarters"
        organisations_form_page.enter_address_line_1("42 Question Road")
        organisations_form_page.enter_region("London")
        organisations_form_page.enter_post_code("Islington")
        organisations_form_page.enter_city("London")
        organisations_form_page.enter_country("Ukraine")
        organisations_form_page.click_submit()
    if not context.org_registered_status:
        organisations_form_page = OrganisationsFormPage(driver)
        organisations_form_page.enter_email("trinity@unicorns.com")
        context.email = "trinity@unicorns.com"
        organisations_form_page.enter_first_name("Trinity")
        organisations_form_page.enter_last_name("Fishburne")
        organisations_form_page.enter_password("12345678900")
        organisations_form_page.click_submit()


@pytest.fixture(scope="session")
def set_up_app_before_hook(driver, request):
    exporter_hub = ExporterHub(driver)
    driver.get(request.config.getoption("--exporter_url"))
    if "login" in driver.current_url:
        exporter_hub.login("trinity@unicorns.com", "12345678900")
    app_set_up(driver, request)


def app_set_up(driver, request):
    exporter_hub = ExporterHub(driver)
    exporter_hub.click_goods_tile()
    exporter_hub.click_add_a_good()
    exporter_hub.enter_description_of_goods("MPG 2.")
    exporter_hub.select_is_your_good_controlled("Yes")
    exporter_hub.enter_control_code("1234")
    exporter_hub.select_is_your_good_intended_to_be_incorporated_into_an_end_product("Yes")
    exporter_hub.enter_part_number("1234")
    exporter_hub.click_save_and_continue()
    driver.get(request.config.getoption("--exporter_url"))
    exporter_hub.click_apply_for_a_licence()
    exporter_hub.click_start_now_btn()
    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id
    app_name = "Test Application " + app_time_id
    exporter_hub.enter_name_or_reference_for_application(app_name)
    context.app_id = app_name
    exporter_hub.click_save_and_continue()
    exporter_hub.click_export_licence("standard")
    exporter_hub.click_continue()
    exporter_hub.click_permanent_or_temporary_button("permanent")
    exporter_hub.click_continue()
    exporter_hub.click_export_licence_yes_or_no("yes")
    exporter_hub.type_into_reference_number("1234")
    exporter_hub.click_continue()
    exporter_hub.click_application_locations_link()
    exporter_hub.click_on_organisation_or_external_radio_button("organisation")
    exporter_hub.click_continue()
    exporter_hub.click_sites_checkbox(int(1) - 1)
    exporter_hub.click_continue()
    driver.execute_script("document.getElementById('goods').scrollIntoView(true);")
    exporter_hub.click_goods_link()
    driver.find_element_by_css_selector('.govuk-button[href*="add-preexisting"]').click()
    driver.find_elements_by_css_selector('a.govuk-button')[int(1) - 1].click()
    exporter_hub.add_values_to_good(str("1"), str("123"), "Metres")
    exporter_hub.click_continue()
    exporter_hub.click_on_overview()
    exporter_hub.click_end_user_link()
    exporter_hub.select_end_user_type("government")
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_name("Mr Smith")
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_website("https://www.smith.com")
    exporter_hub.click_continue()
    exporter_hub.enter_end_user_address("London")
    exporter_hub.enter_end_user_country("Ukraine")
    exporter_hub.click_continue()
    exporter_hub.click_submit_application()


@pytest.fixture(scope="function")
def open_internal_hub(driver, internal_url, sso_sign_in_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to the internal homepage')
def when_go_to_internal_homepage(driver, internal_url):
    driver.get(internal_url)


@given('I go to internal homepage')
def go_to_internal_homepage(driver, internal_url, sso_sign_in_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to internal homepage and sign in')
def go_to_internal_homepage_sign_in(driver, internal_url, sso_sign_in_url):
    driver.get(sso_sign_in_url)
    driver.find_element_by_name("username").send_keys(sso_email)
    driver.find_element_by_name("password").send_keys(sso_password)
    driver.find_element_by_css_selector("[type='submit']").click()
    driver.get(internal_url)


@when('I go to exporter homepage')
def go_to_exporter_when(driver, exporter_url):
    driver.get(exporter_url)


@when(parsers.parse('I login to exporter homepage with username "{username}" and "{password}"'))
def login_to_exporter(driver, username, password, set_up_org):
    if username == "TestBusinessForSites@mail.com":
        username = context.email
    exporter_hub = ExporterHub(driver)
    if "login" in driver.current_url:
        exporter_hub.login(username, password)


@when('I click on application previously created')
def click_on_created_application(driver, set_up_app_before_hook, internal_url):
    driver.get(internal_url)
    driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()


@when('I click on an application previously created')
def click_on_a_created_application(driver):
    driver.find_element_by_css_selector(".lite-cases-table a[href*='/cases/']").click()


@when('I click submit button')
def click_on_submit_button(driver):
    shared = Shared(driver)
    shared.click_submit()


@then(parsers.parse('I see error message "{expected_error}"'))
def error_message_shared(driver, expected_error):
    shared = Shared(driver)
    assert expected_error in shared.get_text_of_error_message()


@when('I click sites link')
def i_click_sites_link(driver):
    exporter = ExporterHub(driver)
    exporter.click_sites_link()


@when('I click new site')
def click_new_site(driver):
    exporter = ExporterHub(driver)
    exporter.click_new_sites_link()


@when('I click continue')
def i_click_continue(driver):
    driver.find_element_by_css_selector("button[type*='submit']").click()

@when('I go to flags')
def go_to_flags(driver):
    header = HeaderPage(driver)

    header.click_lite_menu()
    header.click_flags()


@when(parsers.parse('I add a flag called "{flag_name}" at level "{flag_level}"'))
def add_a_flag(driver, flag_name, flag_level):
    flags_page = FlagsPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()
    flags_page.click_add_a_flag_button()
    if flag_name == " ":
        context.flag_name = flag_name
    else:
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string))-7:]
        context.flag_name = flag_name + extra_string
    flags_page.enter_flag_name(context.flag_name)
    flags_page.select_flag_level(flag_level)
    shared.click_submit()
