@internal @give_advice
Feature: I want to record my user advice and any comments and conditions relating to my recommendation
  As a logged in government user working on a specific case that is assigned to me
  I want to record my user advice and any comments and conditions relating to my recommendation
  So that other users can see my decision and know that I have finished assessing this case

  @LT_1376_grant
  Scenario: Give advice and grant a licence
    Given I create application or application has been previously created
    And I have created a proviso picklist
    And I have created an advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And  I click on view advice
    And I select "2" items in the advice view
    And I choose to "Grant the licence"
    And I import text from the "advice" picklist
    And I write "We will get back to you in three weeks" in the note text field
    And I go back to the advice screen
    Then I see added advice in "2" places

  @LT_1376_proviso
  Scenario: Give advice and add a proviso
    Given I create application or application has been previously created
    And I have created a proviso picklist
    And I have created an advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And  I click on view advice
    And I select "2" items in the advice view
    And I choose to "Add a proviso"
    And I import text from the "proviso" picklist
    And I import text from the "advice" picklist
    And I write "We will get back to you in three weeks" in the note text field
    And I go back to the advice screen
    Then I see added advice in "2" places

  @LT_1376_deny
  Scenario: Give advice and deny a licence
    Given I create application or application has been previously created
    And I have created a proviso picklist
    And I have created an advice picklist
    And I sign in to SSO or am signed into SSO
    When I go to application previously created
    And  I click on view advice
    And I select "2" items in the advice view
    And I choose to "Refuse the license"
    And I select decision "1a"
    And I select decision "2b"
    And I import text from the "advice" picklist
    And I write "We will get back to you in three weeks" in the note text field
    And I go back to the advice screen
    Then I see added advice in "2" places
