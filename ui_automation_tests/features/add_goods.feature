@goods @all
Feature: I want to add a clc-case good to the goods list
    As a logged in exporter
    I want to add a clc-case good to the goods list
    So that I can ensure the good is listed in my cases

    @LT_1006_add_clc_query_good
    Scenario: Add "I don't know" good
        Given I go to internal homepage
        Then I see the clc-case previously created
