Feature: I want to add and manage users
  As a logged in government user
  I want to add and manage users
  So that an there are caseworkers belonging to different teams to casework a case

  Scenario: Add a user
    Given I go to internal homepage
    When I go to users
    And I choose to add a user
    And I add a user with email: "test@mail.com" and team in position 1
    Then I see the newly added user

  Scenario: Fail to add a user
    Given I go to internal homepage
    When I go to users
    And I choose to add a user
    And I add a duplicate user
    Then I see user validation errors