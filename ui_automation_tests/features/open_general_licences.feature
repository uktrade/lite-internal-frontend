@all @internal @open_general_licences
Feature: I want to add open general licences
    So that exporters can use them

  @lt_1268_open_general_licences @regression
  Scenario: Add an open general licence, edit it and deactivate it
    Given I sign in to SSO or am signed into SSO
    When I go to open general licences
    And I click the new open general licence button
    And I select Open General Export Licence
    And I fill in details about the licence
    And I select the tree Controlled Radioactive Sources
    And I select the country United Kingdom
    Then I see the summary list
    When I click submit
    Then I see the newly generated open general export licence
