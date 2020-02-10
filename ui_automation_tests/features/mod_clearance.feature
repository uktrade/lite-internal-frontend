@all
Feature: View an MOD Clearance

  @smoke @MOD
  Scenario: View an Exhibition Clearance
    Given I go to internal homepage
    And an Exhibition Clearance is created
    When I show filters
    When filter case type has been changed to "MOD Exhibition Clearance"
    When I click on the MOD Clearance case
    Then I see the MOD Clearance case page

  @smoke @MOD
  Scenario: View an F680 Clearance
    Given I go to internal homepage
    And an F680 Clearance is created
    When I show filters
    When filter case type has been changed to "MOD F680 Clearance"
    When I click on the MOD Clearance case
    Then I see the MOD Clearance case page

  @smoke @MOD
  Scenario: View an Gifting Clearance
    Given I go to internal homepage
    And an Gifting Clearance is created
    When I show filters
    When filter case type has been changed to "MOD Gifting Clearance"
    When I click on the MOD Clearance case
    Then I see the MOD Clearance case page
