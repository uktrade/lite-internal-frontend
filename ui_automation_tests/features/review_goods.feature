@internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT_1300
  Scenario: Add flag to good
    Given I sign in to SSO or am signed into SSO
    And I create application or application has been previously created
    When I go to application previously created
    And I select goods and click review
    And I click on add report summary
    And  I respond "yes", "ML4b1", "0", "Because the good is controlled" and click continue
    Then the control list is present on goods review page
