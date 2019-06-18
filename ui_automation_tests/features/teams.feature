Feature: I want to add teams
  As a logged in government user
  I want to add teams
  So that an application/query can be directed to one or more teams, and progressed through those teams

  Scenario: Add a department
    Given I go to internal homepage
    When I go to teams
    When I add a team called "DIT"
    Then I see the team in the team list