from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages
import helpers.helpers as utils
from conftest import context

scenarios('../features/teams.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@when('I go to teams')
def go_to_teams(driver):
    header = HeaderPage(driver)

    header.click_lite_menu()
    header.click_teams()


@when(parsers.parse('I add a team called "{team_name}"'))
def add_a_team(driver, team_name):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()
    teams_pages.click_add_a_team_button()
    context.team_name = team_name + str(utils.get_unformatted_date_time())
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@then('I see the team in the team list')
def see_team_in_list(driver):
    team_name = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.team_name + "')]]")
    assert team_name.is_displayed()
