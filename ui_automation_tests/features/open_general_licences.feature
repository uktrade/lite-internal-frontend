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
    And I open the open general licence
    Then I see the new open general export licence
    When I click change name
    And I change the OGL name
    Then I see the updated open general export licence
    When I deactivate the open general licence
    Then I see the updated open general export licence


  @lt_1470_open_general_licences @regression
  Scenario: Add an open general licence application and view it
    Given I sign in to SSO or am signed into SSO
    And an ogel licence has been added
    And an ogel application has been added
    When I filter by OGEL type
    And I click on first case
    Then I see OGEL case
