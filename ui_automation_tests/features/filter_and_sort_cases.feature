@all @internal @filter_and_sort
Feature: I want to filter and sort cases on a queue
  As a logged in government user
  I want to filter and sort the cases in the work queue I am viewing
  So that I can easily find the cases I am most interested in

  @LT_914_filter_and_sort @smoke
  Scenario: Filter and sort
    Given I sign in to SSO or am signed into SSO
    And a queue has been created
    And I create open application or open application has been previously created
    And case has been moved to new Queue
    And I create a clc query
    And I go to internal homepage
    When case has been moved to new Queue
    And I click on new queue in dropdown
    Then "2" cases are shown
    When I show filters
    When filter status has been changed to "Finalised"
    Then there are no cases shown
    When I click clear filters
    When I show filters
    When filter case type has been changed to "Goods Query"
    Then "1" cases are shown
    When filter status has been changed to "CLC review"
    Then "1" cases are shown
    When I click clear filters
    Then "2" cases are shown
    When I go to application previously created
    And I click progress application
    And I select status "Under review" and save
    And I go to the internal homepage
    And I click on new queue in dropdown
    And I sort cases by status
    # Application is removed due to case routing rules and change of status
    Then "1" cases are shown
    And the case at index "0" has the status of "CLC review"
    When I show filters
    And I click filter to show cases with open team ecju queries
    Then "1" cases are shown

#  @LT_914_sort_all_cases @regression
#  Scenario: Sort all cases
#    Given I sign in to SSO or am signed into SSO
#    And I create open application or open application has been previously created
#    And I go to internal homepage
#    When I click on the "All cases" queue in dropdown
#    And I sort cases by status
#    Then the case at index "0" has the status of "Submitted"

  @LT_914_filter_and_sort @regression
  Scenario: I can show and hide filters
    Given I sign in to SSO or am signed into SSO
    And I go to internal homepage
    When I show filters
    Then the filters are shown
    When I hide filters
    Then the filters are hidden
