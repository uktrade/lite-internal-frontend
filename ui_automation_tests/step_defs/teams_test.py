from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages
import helpers.helpers as utils

scenarios('../features/teams.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I go to teams')
def go_to_teams(driver):
    header = HeaderPage(driver)
    shared = Shared(driver)

    header.click_lite_menu()
    header.click_teams()
    shared.click_submit()


@when(parsers.parse('I add a team called "{team_name}"'))
def add_a_team(driver, team_name):
    teams_pages = TeamsPages(driver)
    utils.get_unformatted_date_time()
    teams_pages.enter_team_name(team_name + utils.get_unformatted_date_time())


@then(parsers.parse('I see the team in the team list"'))
def add_a_team(driver, team_name):
    teams_pages = TeamsPages(driver)
    teams_pages.enter_team_name(team_name)