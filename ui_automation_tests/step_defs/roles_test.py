from pytest_bdd import scenarios, when, parsers

from pages.users_page import UsersPage
from pages.roles_pages import RolesPages
from pages.shared import Shared

import helpers.helpers as utils

from ui_automation_tests.conftest import context

scenarios('../features/flags.feature', strict_gherkin=False)

import logging

log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@when('I go to manage roles')
def go_to_manage_roles(driver):
    user_page = UsersPage(driver)

    user_page.click_manage_roles()

@when(parsers.parse('I add a new role called "{role_name}" with permission to "{permissions}"'))
def add_a_role(driver, role_name, permissions):
    roles_page = RolesPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()

    roles_page.click_add_role()
    if role_name == " ":
        context.role_name = role_name
    else:
        extra_string = str(utils.get_unformatted_date_time())
        extra_string = extra_string[(len(extra_string))-14:]
        context.role_name = role_name + extra_string

    roles_page.enter_role_name(context.role_name)
    roles_page.select_permissions(permissions)
    shared.click_submit()


