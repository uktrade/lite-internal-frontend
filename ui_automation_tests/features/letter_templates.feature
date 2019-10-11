@internal @templates
Feature: I want to configure standard templates for letter generation
As a logged in government user
I want to configure standard templates for letter generation
So that I can create standard letters used by case workers and they can be updated when required

  @LT_1029_add_template
  Scenario: Add template
    Given I go to internal homepage
    And I create a letter paragraph picklist
    When I go to letters
    And I create a letter template
    And I add a letter paragraph to template
    Then I see the drag and drop page
    When I preview template
    Then my picklist is in template
    When I click save
    Then I see my template in the table
    When I edit my template
    Then I see my template in the table
