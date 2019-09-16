@internal @clc_query
Feature: I want to respond to clc queries
  As a technical assessment unit officer
  I want to respond to a CLC query with the correct control list classification code to use for a good  or an NLR as applicable
  So that an exporter can apply for a licence with that code and without me needing to assess the goods again

  @LT_1138_respond
  Scenario: respond to a clc type case
    Given I create clc query or clc query has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click Respond to query
    And I respond "yes", "pa3q", "2", "Because the good is controlled" and click continue
    And I submit response
    Then I see case is closed
