from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages
import helpers.helpers as utils
from conftest import context

from pages.users_index_page import UsersIndexPage

scenarios('../features/users.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)

@when('I go to users')
def i_go_to_users(driver):
    header = HeaderPage(driver)

    header.click_lite_menu()
    header.click_users()

@when('I choose to add a user')
def i_choose_to_add_a_user(driver):
    users_page = UsersIndexPage(driver)