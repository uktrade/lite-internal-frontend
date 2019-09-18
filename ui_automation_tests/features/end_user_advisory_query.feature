@internal @eua_query
Feature: I want to respond to an End User Advisory query
  As a logged in government user
  I want to respond to an End User Advisory query
  So that I can inform an exporter whether or not an entity is a suitable end user for a potential export licence

  @LT_1474_respond
    @MSTG
  Scenario: I want to check that the functionality of other cases exists
    Given I sign in to SSO or am signed into SSO
    When I go to eua query previously created
    Then I should see flags can be added
    And I should see the ability to add case notes
    And The dropdown should contain Move Case, Documents, and Ecju queries
