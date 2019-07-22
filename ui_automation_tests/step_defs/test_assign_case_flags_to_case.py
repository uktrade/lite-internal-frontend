import logging
import helpers.helpers as utils
from pages.shared import Shared
from pytest_bdd import given, when, then, scenarios
from pages.flags_pages import FlagsPages
from pages.assign_flags_to_case import CaseFlagsPages
from pages.application_page import ApplicationPage
from pages.header_page import HeaderPage

scenarios('../features/assign_case_flags_to_case.feature', strict_gherkin=False)

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

flags = [{'name': 'flag 1', 'level': 'Case'}, {'name': 'flag2', 'level': 'Case'}]


# TODO: Replace with API fixture to create flags to remove test dependency
@given('Case flags have been created')
def case_flags_have_been_created(driver):
    header = HeaderPage(driver)
    header.click_lite_menu()
    header.click_flags()
    flags_page = FlagsPages(driver)

    shared = Shared(driver)

    for flag in flags:
        flags_page.click_add_a_flag_button()
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string)) - 7:]
        flag['name'] = flag['name'] + extra_string
        flags_page.enter_flag_name(flag['name'])
        flags_page.select_flag_level(flag['level'])
        shared.click_submit()


# TODO: Replace with API fixture to assign flags to remove test dependency
@given('I click on application previously created with flags')
def click_on_created_application(driver, context):
    driver.find_element_by_xpath("//*[text()[contains(.,'" + context.app_id + "')]]").click()


@when("I click edit flags link")
def click_edit_flags_link(driver):
    application_page = ApplicationPage(driver)
    application_page.click_edit_case_flags()


@when('I assign flags to the case')
def assign_flags_to_case(driver):
    case_flags_pages = CaseFlagsPages(driver)
    for flag in flags:
        case_flags_pages.assign_flags(flag['name'])
    shared = Shared(driver)
    shared.click_submit()


@when('I remove flags from the case')
def remove_flags_from_case(driver):
    flags.remove({'name': 'flag 1', 'level': 'Case'})
    case_flags_pages = CaseFlagsPages(driver)
    for flag in flags:
        case_flags_pages.assign_flags(flag['name'])
    shared = Shared(driver)
    shared.click_submit()


@then('I can see the flags on the case')
def flags_are_visible_on_case(driver):
    raise NotImplementedError(u'STEP: Then I can see the flags on the case')
