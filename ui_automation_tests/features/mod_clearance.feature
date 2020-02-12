@all
Feature: View an MOD Clearance

  @smoke @MOD
  Scenario: View an Exhibition Clearance
    Given I sign in to SSO or am signed into SSO
    And an Exhibition Clearance is created
    When I go to the case
    Then I see the MOD Clearance case page

  @regression @MOD
  Scenario: View an F680 Clearance
    Given I sign in to SSO or am signed into SSO
    And an F680 Clearance is created
    When I go to the case
    Then I see the MOD Clearance case page

  @regression @MOD
  Scenario: View an Gifting Clearance
    Given I sign in to SSO or am signed into SSO
    And  an Gifting Clearance is created
    When I go to the case
    Then I see the MOD Clearance case page
