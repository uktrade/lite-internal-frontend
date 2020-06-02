@all @internal @case_flags
Feature: I want to add case-level flags to a case and view them
  As a logged in government user
  I want to toggle one or more flags on and off a case to highlight key features
  So that all users viewing the case can quickly and easily see the aspects which might require more attention

  @LT_949_add @LT_951 @regression @nicky
  Scenario: Add flag to case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I add a flag at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    And I click edit flags link
    Then The previously created flag is assigned to the case
    When I go to the internal homepage
    Then I see previously created application
    And I see the added flags on the queue

  @LT_1185_add @LT_951 @regression
  Scenario: Add flag to good
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I add a flag at level Good
    And I go to application previously created
    And I click edit flags on the first good
    And I select previously created flag
    Then the previously created goods flag is assigned to the good
    When I go to the internal homepage
    Then I see previously created application
    And I see the added flags on the queue

  @LT_951 @regression
  Scenario: Add all flags to case
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    When I add a flag at level Good
    And I go to application previously created
    And I click edit flags on the first good
    And I select previously created flag
    And I add a flag at level Case
    And I go to application previously created
    And I click edit flags link
    And I select previously created flag
    And I add a flag at level Destination
    And I go to application previously created
    And I click edit flags on the first destination
    And I select previously created flag
    And I add a flag at level Organisation
    And I go to application previously created
    And I go to the organisation which submitted the case
    And I click the edit flags link
    And I select previously created flag
    And I go to the internal homepage
    Then I see previously created application
    Then I see 3 flags for the case
    When I click the expand flags dropdown
    Then I see all flags for the case
