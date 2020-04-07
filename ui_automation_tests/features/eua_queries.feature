@all @internal @eua_query
Feature: I want to respond to an End User Advisory query
  As a logged in government user
  I want to respond to an End User Advisory query
  So that I can inform an exporter whether or not an entity is a suitable end user for a potential export licence

  @LT_1474_respond @smoke
  Scenario: I want to check that the functionality of other cases exists
    Given I sign in to SSO or am signed into SSO
    And I create eua query or eua query has been previously created
    When I go to end user advisory previously created
    Then I should see the ability to add case notes
    And The dropdown should contain Move Case, Documents, and Ecju queries

  @LT_1474_change_case_status @regression
  Scenario: I want to check that the case status can be changed
    Given I create eua query or eua query has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to end user advisory previously created
    And I click progress application
    And I select status "Closed" and save
    Then the status has been changed in the end user advisory
