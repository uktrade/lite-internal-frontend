from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from selenium.webdriver.support.ui import Select
from conftest import context
import helpers.helpers as utils
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages

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


@when('I go to users')
def go_to_users(driver):
    header = HeaderPage(driver)
    header.open_users()


@when('I click on my team')
def click_on_my_team(driver):
    driver.find_element_by_link_text(context.team_name).click()


@when('I select my newly created team')
def select_team(driver):
    select = Select(driver.find_element_by_id('team'))
    select.select_by_visible_text(context.team_name)
    Shared(driver).click_submit()


@when('I select Admin team')
def select_team(driver):
    select = Select(driver.find_element_by_id('team'))
    select.select_by_visible_text("Admin")
    Shared(driver).click_submit()


@when('I click edit for my user')
def click_edit_for_my_user(driver):
    driver.find_element_by_xpath("//td[text()='test-uat-user@digital.trade.gov.uk']/following-sibling::td[last()]/a").click()


@when(parsers.parse('I add a team called "{team_name}"'))
def add_a_team(driver, team_name):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    utils.get_unformatted_date_time()
    teams_pages.click_add_a_team_button()
    if team_name == " ":
        context.team_name = team_name
    else:
        context.team_name = team_name + str(utils.get_unformatted_date_time())
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@when('I add an existing team name')
def add_existing_team(driver):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    teams_pages.click_add_a_team_button()
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@when('I edit my team')
def edit_existing_team(driver):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    elements = driver.find_elements_by_css_selector(".govuk-table__cell")
    status = False
    for element in elements:
        if status:
            element.click()
        if element.text == context.team_name:
            status = True
    teams_pages.click_add_a_team_button()
    context.team_name = context.team_name + "edited"
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@then('I see the team in the team list')
def see_team_in_list(driver):
    team_name = driver.find_element_by_xpath("//*[text()[contains(.,'" + context.team_name + "')]]")
    assert team_name.is_displayed()


@then(parsers.parse('I see my teams user list with user "{added_not_added}"'))
def see_team_user_added(driver, added_not_added):
    assert driver.find_element_by_tag_name("h1").text == context.team_name , "User is not on teams user list"
    assert driver.find_element_by_css_selector(".lite-tabs__tab.selected").text == "USERS" , "Users tab isn't shown"
    if added_not_added == "added":
        assert "first-name last-name"	in driver.find_element_by_css_selector(".govuk-table__body").text, "User is not displayed in team list"
        assert "test-uat-user@digital.trade.gov.uk"	in driver.find_element_by_css_selector(".govuk-table__body").text, "User is not displayed in team list"
        assert "Active"	in driver.find_element_by_css_selector(".govuk-table__body").text, "User is not displayed in team list"
    elif added_not_added == "not added":
        assert driver.find_element_by_css_selector(".govuk-caption-l").text == "You don't have any users at the moment." , "Users are potentially displayed for a just created Team List"
