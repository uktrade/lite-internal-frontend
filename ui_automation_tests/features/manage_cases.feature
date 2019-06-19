Feature: Manage cases
  As a..

  Scenario: Change status to Under Review
    Given I go to internal homepage
    When I click on application previously created
    When I click progress application
    When I select status "Under review" and save
    Then the status has been changed in the application
    Then the application headers and information are correct
    #TODO remove dependency here
    When I go to exporter homepage
    When I login to exporter homepage with username "trinity@unicorns.com" and "12345678900"
    When I click applications
    Then the status has been changed in exporter

  Scenario: Record decision
    Given I go to internal homepage
    When I click on application previously created
    When I click record decision
