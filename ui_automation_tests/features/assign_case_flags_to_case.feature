@internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT_949_add
  Scenario: Add flag to case
    Given I create application or application has been previously created
    And I go to flags
    When I add a flag called UAE at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    Then The previously created flag is assigned to the case

  @LT_1185_add
  Scenario: Add flag to good
    Given I create application or application has been previously created
    And I go to flags
    When I add a flag called Suspicious at level Good
    And I go to application previously created
    And I select goods and click review
    And I click edit goods flags link
    And I select previously created flag
    And I click back
    Then the previously created goods flag is assigned to the case
