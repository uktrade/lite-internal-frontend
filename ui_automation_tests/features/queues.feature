@internal @queues
Feature: I want to define new work queues and the teams they belong to
  As a logged in government user
  I want to be able to define new work queues and the department they belong to
  So that new government departments and teams within departments which require their own work queues can easily have one


#  @LT-919_add
#  Scenario: Add and edit a new queue
#    Given I go to internal homepage
#    When I go to queues
#    And I click on add a queue
#    And I enter in queue name "Ready for Review"
#    Then I see the new queue
#    When I go to the internal homepage
#    And I click on new queue in dropdown
#
#  @LT-919_edit
#  Scenario: Edit a new queue
#    Given I go to internal homepage
#    When I go to queues
#    And I click on add a queue
#    And I enter in queue name "Ready for Edit"
#    And I edit the new queue
#    Then I see the new queue
#    When I go to the internal homepage
#    And I click on new queue in dropdown
#
#  @LT-919_empty_validation
#  Scenario: Add empty queue
#    Given I go to internal homepage
#    When I go to queues
#    And I click on add a queue
#    And I enter in queue name " "
#    Then I see error message "Give the queue a valid name"

  @LT-1125_move_cases
  Scenario: Move case to new queue and remove from new queue
    Given I go to internal homepage
    When I go to queues
    And I click on add a queue
    And I enter in queue name "Queue to move case to"
    And I go to the internal homepage
    And I click on application previously created
    And I move case to new queue
    And I go to the internal homepage
    And I click on new queue in dropdown
    Then I see previously created application
    When I click on application previously created
    And I move case to new cases original queue and remove from new queue
    And I go to the internal homepage
    And I click on new queue in dropdown
    Then I dont see previously created application

  @LT-1125
  Scenario: Move cases error message when not selecting any queues
    Given I go to internal homepage
    When I click on application previously created
    And I deselect all queues
    Then I see error message "Select at least one queue"