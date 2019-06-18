@internal @set_up  @all @organisation
Feature: Set up a organisation
As a...

  Scenario: Set up organisation
    Given I go to internal homepage
    When I go to organisations
    When I choose to add a new organisation
    When I provide company registration details of name: "Unicorns Ltd", EORI: "1234567890AAA", SIC: "2345", VAT: "GB1234567", CRN: "09876543"
    When I setup an intial site with name: "Headquarters", addres line 1: "42 Question Road", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    When I setup the admin user with email: "trinity@unicorns.com", first name: "Trinity", last name: "Fishburne", password: "12345678900"
    Then organisation is registered