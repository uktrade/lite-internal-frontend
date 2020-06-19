@all @users
Feature: I want to test users

  @deactivate_user @regression
  Scenario: Add user, deactivate then reactivate
    Given I sign in to SSO or am signed into SSO
    When I go to users
    When I add a new user
    And I show filters
    And I change the user filter to "Active"
    Then I see new user
    When I deactivate new user
    And I show filters
    And I change the user filter to "Active"
    Then I dont see new user
    When I change the user filter to "All"
    Then I see new user
    When I reactivate new user
    And I show filters
    And I change the user filter to "Active"
    Then I see new user
    When I change the user filter to "All"
    Then I see new user
    When I go to teams
    And I add a team called BlueOcean
    Then I see the team in the team list
    When I click on the team BlueOcean
    Then I see my teams user list with user "not added"
    When I go to users
    And I go to edit new user
    And I select my newly created team
    And I click on the team BlueOcean
    Then I see my teams user list with user "added"


  @edit_users @regression
  Scenario: Edit user
    Given I sign in to SSO or am signed into SSO
    When I go to users
    And I add a new user
    And I go to edit new user
    And I edit new users email
    Then the user's profile is updated

  @LT_930_edit @regression
  Scenario: Edit a team
    Given I sign in to SSO or am signed into SSO
    When I go to teams
    And I add a team called BlueOcean
    And I edit my team
    Then I see the team in the team list
