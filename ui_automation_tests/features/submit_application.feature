@exporter @all @setup
Feature: Licence
  As a...

  Scenario: Submit application
    Given I go to exporter homepage
    When I login to exporter homepage with username "test@mail.com" and "password"
    When I click on goods tile
    When I add a good with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
    When I go to exporter homepage
    When I click on apply for a license button
    When I click on start button
    When I enter in name for application and continue
    When I select "standard" application and continue
    When I select "permanent" option and continue
    When I select "yes" for whether I have an export licence and "123456" if I have a reference and continue
    When I click on application locations link
    When I select "organisation" for where my goods are located
    When I select the site at position "1"
    When I click continue
    When I click on the goods link from overview
    When I click the add from organisations goods button
    When I click add to application for the good at position "1"
    When I add values to my good of "1" quantity "123" and unit of measurement "Metres"
    When I click continue
    Then good is added to application
    When I click overview
    When I click on end user
    When I add an end user of type: "government", name: "Mr Smith", website: "https://www.smith.com", address: "London" and country "Ukraine"
    When I submit the application
    Then application is submitted
