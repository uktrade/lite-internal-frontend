@all @MOD
Feature: View an Open Applications

  @smoke @open_application
  Scenario: View an Open Application
    Given I sign in to SSO or am signed into SSO
    And I create open application or open application has been previously created
    Then I should see my case in the cases list
    When I go to the case
    Then I see the Open Application case page
