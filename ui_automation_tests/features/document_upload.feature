@internal
Feature: I want to attach related documents to a case and view attached documents
As a logged in government user
I want to attach related documents to a case and view attached documents
So that it is recorded against the case and available for other case workers to view

@LT-945_upload
Scenario: Upload a new document that doesn't contain a virus
  Given I go to internal homepage
  When I click on application previously created
  And I click on the Documents button
  And I click on the Attach Document button
  And I upload a file
  Then the file is listed on the Documents page
