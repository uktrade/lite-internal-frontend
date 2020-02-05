@all @internal @goods_query
Feature: I want to respond to clc queries
  As a technical assessment unit officer
  I want to respond to a CLC query with the correct control list classification code to use for a good  or an NLR as applicable
  So that an exporter can apply for a licence with that code and without me needing to assess the goods again

  @LT_1138_respond @clc @smoke
  Scenario: respond to a clc type of query
    Given I sign in to SSO or am signed into SSO
    And I create report summary picklist
    And I create a clc query
    When I go to goods query previously created
    And I click Respond to clc query
    And I respond "yes", "ML1a", "1", "Because the good is controlled" and click continue
    And I submit response
    When I click progress application
    And I select status "Closed" and save
    Then I see case is closed
    When I click progress application
    And I select status "Withdrawn" and save
    Then the status has been changed in the application

  @LT_1528_respond @pv_grading @smoke
  Scenario: respond to a grading type of query
    Given I sign in to SSO or am signed into SSO
    And I create report summary picklist
    And I create a grading query
    When I go to goods query previously created
    And I click Respond to grading query
    And I respond prefix "abc", select "UK official", suffix "123", comment "This is my review", and click continue
    And I submit response
    When I click progress application
    And I select status "Closed" and save
    Then I see case is closed
    When I click progress application
    And I select status "Withdrawn" and save
    Then the status has been changed in the application
