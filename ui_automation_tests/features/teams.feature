Feature: I want to add teams
  As a logged in government user
  I want to add teams
  So that an application/query can be directed to one or more teams, and progressed through those teams

  Scenario: Add a team and then try to add same team name
    Given I go to internal homepage
    When I go to teams
    And I add a team called "DIT"
    Then I see the team in the team list
    When I add an existing team name
    Then I see error message "Enter a name which is not already in use by another team"

  Scenario: Add a team and click on team name and add user to team and rollback
    Given I go to internal homepage
    When I go to teams
    And I add a team called "DIT"
    When I click on my team
    Then I see my teams user list with user "not added"
    When I go to users
    And I click edit for my user
    And I select my newly created team
    And I click on my team
    Then I see my teams user list with user "added"
    When I click edit for my user
    And I select Admin team

  Scenario: Add a team with empty field
    Given I go to internal homepage
    When I go to teams
    And I add a team called " "
    Then I see error message "Team name may not be blank"

  Scenario: Add a team with over 50 characters field
    Given I go to internal homepage
    When I go to teams
    And I add a team called "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    Then I see error message "Ensure this field has no more than 50 characters."

  Scenario: Edit a team
    Given I go to internal homepage
    When I go to teams
    And I add a team called "Team to edit"
    And I edit my team
    Then I see the team in the team list
