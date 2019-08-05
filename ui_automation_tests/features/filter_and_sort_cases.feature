@internal @filter_and_sort
Feature: I want to filter and sort cases on a queue
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
    When filter status has been changed to "approved"
    Then there are no cases shown
    When I show filters
    When filter case type has been changed to "ClC query"
    Then "1" cases are shown
    When Filter status has been changed to "submitted"
    Then "1" cases are shown
    When I show filters
    And I click clear filters
    Then "2" cases are shown
    When I click on application previously created
    And I click progress application
    And I select status "Under review" and save
    When I go to internal homepage
    When I click on new queue in dropdown
    When I sort cases by "Status"
    Then the cases are in order of "Status"
    When I show filters
    When I hide filters
    Then the filters are no longer shown
