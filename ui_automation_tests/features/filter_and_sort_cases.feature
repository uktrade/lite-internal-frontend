@internal @filter_and_sort
Feature:  I want to filter and sort cases on a queue
  As a logged in government user
  I want to filter and sort the cases in the work queue I am viewing
  So that I can easily find the cases I am most interested in

  @LT_914_filter_and_sort
  Scenario: Filter and sort
    Given Queue has been created
    And I create application or application has been previously created
    And I go to internal homepage
    When Case has been moved to new Queue
    And I create a clc_query
    And Case has been moved to new Queue
    And I click on new queue in dropdown
    Then "2" cases are shown
    When I show filters
    And Filter status has been changed to "approved"
    Then There are no cases shown
    When I show filters
    And Filter case type has been changed to "ClC query"
    Then "1" cases are shown
    When Filter status has been changed to "submitted"
    Then "1" cases are shown
    When I show filters
    And I click clear filters
    Then "2" cases are shown
    When I click on application previously created
    And I click progress application
    And I select status "Under review" and save
    And I go to internal homepage
    And I click on new queue in dropdown
    And I sort cases by status
    Then Cases are in order
    When I show filters
    And I hide filters
    Then Filter dropdowns are no longer shown
