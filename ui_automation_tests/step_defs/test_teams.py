from pytest_bdd import when, then, parsers, scenarios, given
import shared.tools.helpers as utils
from pages.shared import Shared
from pages.teams_pages import TeamsPages
from pages.users_page import UsersPage

scenarios("../features/teams.feature", strict_gherkin=False)


@when("I go to teams")
def go_to_teams(driver, sso_sign_in, internal_url):
    driver.get(internal_url.rstrip("/") + "/teams/")


@when("I click on my team")
def click_on_my_team(driver, context):
    Shared(driver).scroll_to_bottom_row()
    driver.find_element_by_link_text(context.team_name).click()


@when("I select my newly created team")
def select_team(driver, context):
    TeamsPages(driver).select_team_from_dropdown(context.team_name)
    Shared(driver).click_submit()


@when("I select Admin team")
def select_team(driver):
    TeamsPages(driver).select_team_from_dropdown("Admin")
    Shared(driver).click_submit()


@when("I click edit for my user")
def click_edit_for_my_user(driver, internal_info):
    index = utils.get_element_index_by_text(Shared(driver).get_rows_in_lite_table(), internal_info["email"])
    Shared(driver).scroll_to_bottom_row()
    utils.scroll_to_right_of_page(driver)
    UsersPage(driver).click_edit_button_by_index(index)


@when(parsers.parse("I add a team called BlueOcean"))
def add_a_team_blue_ocean(driver, add_a_team, context):
    pass


@when("I edit my team")
def edit_existing_team(driver, context):
    teams_pages = TeamsPages(driver)
    shared = Shared(driver)
    elements = shared.get_links_in_lite_table()
    no = utils.get_element_index_by_text(elements, context.team_name)
    elements[no + 1].click()
    context.team_name = context.team_name + "edited"
    teams_pages.enter_team_name(context.team_name)
    shared.click_submit()


@then("I see the team in the team list")
def see_team_in_list(driver, context):
    assert context.team_name in Shared(driver).get_text_of_lite_table_body()


@then(parsers.parse('I see my teams user list with user "{added_not_added}"'))
def see_team_user_added(driver, added_not_added, context, internal_info):
    assert Shared(driver).get_text_of_h2() == context.team_name, "User is not on teams user list"
    assert Shared(driver).get_text_of_selected_tab() == "USERS", "Users tab isn't shown"
    if added_not_added == "added":
        table = Shared(driver).get_text_of_lite_table_body()
        assert internal_info["name"] in table, "User is not displayed in team list"
        assert internal_info["email"] in table, "User is not displayed in team list"
        assert "Active" in table, "User is not displayed in team list"
    elif added_not_added == "not added":
        assert (
            Shared(driver).get_text_of_caption() == "You don't have any users at the moment."
        ), "Users are potentially displayed for a just created Team List"
