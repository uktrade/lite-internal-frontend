@internal @roles
Feature:  I want to create roles
  As a logged in government user
  I want to create roles with permissions
  So that I can restrict access to functionality

  @LT-1127_add
  Scenario: Create new role
    Given I go to internal homepage
    When I go to users
    When I go to manage roles
    And I add a new role called "role-t" with permission to "Make final decisions"
    Then I see the role in the role list
    When I add an existing role name
    Then I see error message "Enter a name which is not already in use by another role"

  @LT-1127_empty
  Scenario: Add a flag with empty field
    Given I go to internal homepage
    When I go to users
    When I go to manage roles
    And I add a new role called " " with permissions to "Make final decisions"
    Then I see error message "Flag name may not be blank"

  @LT-1127_over
  Scenario: Add a flag with over 20 characters field
    Given I go to internal homepage
    When I go to users
    When I go to manage roles
    And I add a new role called "abcdefghijklmnopqrstuvwxyz12345" with permission to "Make final decisions"
    Then I see error message "Ensure this field has no more than 30 characters."

  @LT-1127_edit @setup
  Scenario: Edit a flag
    Given I go to internal homepage
    When I go to users
    When I go to manage roles
    And I add a new role called "role-t" with permission to "Make final decisions"
    And I edit my role
    Then I see the role in the role list
