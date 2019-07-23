@internal @organisation
Feature: I want to add a company to LITE
As a logged in government user
I want to add a new company to LITE
So that the new company can make applications

  @LT-934_test
  Scenario: Test organisation
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation
    And I provide company registration details of name: "BlueOcean", EORI: "GB987654312000", SIC: "73200", VAT: "123456789", CRN: "000000011"
    And I setup an initial site with name: "HQ", addres line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: "TestBusinessForSites@mail.com", first name: "Trinity", last name: "Fishburne", password: "12345678900"
    Then organisation is registered
    When I go to exporter homepage
    And I login to exporter homepage with username context username and "12345678900"
    And I click sites link
    And I click new site
    And I enter in text for new site "London HQ" "address" "postcode" "city" "region" and "Ukraine"
    And I click continue
    And I go to the internal homepage
    And I go to organisations
    And I click on my registered organisation
    Then my new site is displayed

  @LT-934_error
  Scenario: Organisation registration validation
    Given I go to internal homepage
    When I go to organisations
    And I choose to add a new organisation
    And I provide company registration details of name: " ", EORI: " ", SIC: " ", VAT: " ", CRN: " "
    Then I see error message "This field may not be blank."
    When I provide company registration details of name: "GreenOcean", EORI: "GB987654312000", SIC: "73200", VAT: "123456789", CRN: "000000011"
    And I setup an initial site with name: " ", addres line 1: " ", town or city: " ", County: " ", post code: " ", country: " "
    Then I see error message "This field may not be blank."
    When I setup an initial site with name: "HQ", addres line 1: "123 Cobalt Street", town or city: "London", County: "Islington", post code: "AB1 2CD", country: "Ukraine"
    And I setup the admin user with email: " ", first name: " ", last name: " ", password: " "
    Then I see error message "This field may not be blank."
    When I setup the admin user with email: "TestBusinessABC@mail.com", first name: "Trinity", last name: "Fishburne", password: "12345678900"
    Then organisation is registered
