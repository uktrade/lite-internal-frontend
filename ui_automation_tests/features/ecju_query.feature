@internal @ecju_query
Feature: I want to create ECJU queries
  As a logged in government user
  I want to create ECJU queries
  So that I can clarify the details of a case with the external user

  @LT_1192_add
  @ECF
  Scenario: Add an ECJU Query to a case
    Given I create application or application has been previously created
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    Then I see the ECJU Queries button