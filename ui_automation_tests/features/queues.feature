@all @internal @queues
Feature: I want to define new work queues and the teams they belong to
  As a logged in government user
  I want to be able to define new work queues and the department they belong to
  So that new government departments and teams within departments which require their own work queues can easily have one


  @LT_919_add @regression
  Scenario: Add a new queue
    Given I go to internal homepage
    When I go to queues
    And I enter in queue name Review
    Then I see the new queue
    When I go to the internal homepage
    And I click on new queue in dropdown

  @LT_1125_move_cases @smoke
  Scenario: Move case to new queue and remove from new queue
    Given I create open application or open application has been previously created
    When I go to queues
    And I enter in queue name Review
    And I go to application previously created
    And I add case to newly created queue
    Then I see "1" queue checkboxes selected
    When I go to the internal homepage
    And I click on new queue in dropdown
    Then I see previously created application
    When I go to application previously created
    Then queue change is in audit trail

  @LT_1123_view_all_cases @view_all_cases @regression
  Scenario: Closed cases appear on the all cases queue
    Given I create open application or open application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click progress application
    And I select status "Withdrawn" and save
    And I go to the internal homepage
    And I click on the "All Cases" queue in dropdown
    Then I see previously created application

  @LT_1123_view_all_cases @view_all_cases @regression
  Scenario: Closed cases dont appear on the open cases queue
    Given I create open application or open application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And I click progress application
    And I select status "Withdrawn" and save
    And I go to the internal homepage
    And I click on the "Open Cases" queue in dropdown
    Then I dont see previously created application
    
  @LT_919_edit @regression
  Scenario: Edit a new queue
    Given I go to internal homepage
    When I go to queues
    When I enter in queue name Review
    And I edit the new queue
    Then I see the edited queue
