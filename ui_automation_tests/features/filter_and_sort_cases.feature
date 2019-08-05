@internal @filter_and_sort
Feature:  I want to filter and sort cases on a queue
  As a logged in government user
  I want to filter and sort the cases in the work queue I am viewing
  So that I can easily find the cases I am most interested in

  @LT_914_filter_and_sort
  Scenario: Filter and sort
    Given Queue has been created
#    When I create application or application has been previously created
#    When Case has been moved to new Queue
#    When I create application or application has been previously created
#    When Case has been moved to new Queue
#    When I create a clc_query
#    When Case has been moved to new Queue
#    When I go to internal homepage
#    When I click on new queue in dropdown
#    Then "3" cases appear
#    When I show filters
#    When Filter status has been changed to "approved"
#    Then There are no cases shown
#    When Filter case type has been changed to "ClC query"
#    When Filter status has been changed to "submitted"
#    Then "1" cases are shown
#    When Filter has been cleared
#    Then "3" cases are shown
#    When I click on application previously created
#    And I click progress application
#    And I select status "Under review" and save
#    When I go to internal homepage
#    When I click on new queue in dropdown
#    When I sort cases by status
#    Then Cases are in order
#    When I hide filters
#    Then Filter dropdowns are no longer shown
