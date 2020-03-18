@all @internal @additional_contacts
Feature: I want to add additional contacts to a case
    So that all information is available about a case

  @LT_1253_Additional_contacts @regression
  Scenario: Add an additional contact to a case
    Given I sign in to SSO or am signed into SSO
    And I create standard application or standard application has been previously created
    When I go to application previously created
    And I click on the additional contacts button
    And I click the add button
    And I fill in the details and submit
    Then I can see the new contact in the list
