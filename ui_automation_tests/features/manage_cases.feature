<<<<<<< HEAD
Feature: Manage cases
  As a..

  Scenario: Manage cases
    Given I go to internal homepage
    When I click on application previously created
    When I click progress application
    When I select status "Under review" and save
    Then the status has been changed in the header
    #TODO remove dependency here
    When I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click applications
    Then the status has been changed in exporter
