@internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT-949_add
  Scenario: Add flag to case
    Given I go to internal homepage
    And Case flags have been created
    When I click on application previously created
    When I click edit flags link
    And I assign flags to the case
    Then I can see the flags on the case


  @LT-949_remove
  Scenario: Remove flag from case
    Given I click on application previously created with flags
    When I click edit flags link
    And I remove flags from the case
    Then I can see the flags on the case