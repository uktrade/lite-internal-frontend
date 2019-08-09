from pytest_bdd import when, then, parsers, scenarios
from pages.application_page import ApplicationPage
from pages.record_decision_page import RecordDecision
from pages.shared import Shared
import helpers.helpers as utils

from ui_automation_tests.pages.roles_pages import RolesPages

from pages.header_page import HeaderPage
from ui_automation_tests.pages.users_page import UsersPage


class ManageCases():
    scenarios('../features/manage_cases.feature', strict_gherkin=False)

    import logging
    log = logging.getLogger()
    console = logging.StreamHandler()
    log.addHandler(console)

    @when('I click record decision')
    def click_post_note(driver, context):
        ApplicationPage(driver).click_record_decision()
        context.decision_array = []

    @when(parsers.parse('I "{grant_or_deny}" application'))
    def grant_or_deny_decision(driver, grant_or_deny):
        record = RecordDecision(driver)
        if grant_or_deny == "grant":
            record.click_on_grant_licence()
        elif grant_or_deny == "deny":
            record.click_on_deny_licence()

    @when(parsers.parse('I type optional text "{optional_text}"'))
    def type_optional_text(driver, optional_text, context):
        record = RecordDecision(driver)
        record.enter_optional_text(optional_text)
        context.optional_text = optional_text

    @when(parsers.parse('I select decision "{number}"'))
    def select_decision(driver, number, context):
        record = RecordDecision(driver)
        record.click_on_decision_number(number)
        context.decision_array.append(number)

    @then(parsers.parse('I see application "{grant_or_deny}"'))
    def see_application_granted_or_denied(driver, grant_or_deny, context):
        record = RecordDecision(driver)
        application_page = ApplicationPage(driver)

        if grant_or_deny == "granted":
            assert "set the status to approved" in application_page.get_text_of_audit_trail_item(0), "status has not been shown as approved in audit trail"
        elif grant_or_deny == "denied":
            assert "set the status to under final review" in application_page.get_text_of_audit_trail_item(0), "status has not been shown as under review in audit trail"
            try:
                assert record.get_text_of_denial_reasons_headers(1) == "Further information"
                assert record.get_text_of_denial_reasons_listed(6) == context.optional_text
            except AttributeError:
                pass
            except IndexError:
                pass
            assert record.get_text_of_denial_reasons_headers(0) == "This case was denied because"
            i = 5
            for denial_reason_code in context.decision_array:
                assert record.get_text_of_denial_reasons_listed(i) == denial_reason_code
                i += 1

    @then('the status has been changed in the application')
    def status_has_been_changed_in_header(driver, context, sso_users_name):
        application_page = ApplicationPage(driver)
        assert "set the status to " + context.status.lower in application_page.get_text_of_audit_trail_item(0), "status has not been shown as approved in audit trail"
        # this also tests that the activities are in reverse chronological order as it is expecting the status change to be first.
        assert utils.search_for_correct_date_regex_in_element(application_page.get_text_of_activity_dates(0)), "date is not displayed after status change"
        assert application_page.get_text_of_activity_users(0) == sso_users_name, "user who has made the status change has not been displayed correctly"

    @then('the application headers and information are correct')
    def application_headers_and_info_are_correct(driver, api_url, context):
        application_page = ApplicationPage(driver)
        application_summary = application_page.get_text_of_application_summary_board()
        assert "APPLICANT" in application_summary
        assert "ACTIVITY" in application_summary
        assert "CREATED AT" in application_summary
        assert "REFERENCE NUMBER" in application_summary
        assert "LICENCE TYPE" in application_summary
        assert "LAST UPDATED" in application_summary
        assert context.org_name in application_summary
        assert "Trading" in application_summary or "Brokering" in application_summary
        assert context.date_time_of_update in application_summary
        assert "None" in application_summary
        assert "Standard licence" in application_summary

    @when(parsers.parse('I give myself the required permissions for "{permission}"'))
    def get_required_permissions(driver, permission):
        roles_page = RolesPages(driver)
        HeaderPage(driver).open_users()
        UsersPage(driver).click_on_manage_roles()
        roles_page.click_edit_for_default_role()
        roles_page.edit_default_role_to_have_permission(permission)
        Shared(driver).click_submit()

    @then("I reset the permissions")
    def reset_permissions(driver):
        roles_page = RolesPages(driver)
        HeaderPage(driver).open_users()
        UsersPage(driver).click_on_manage_roles()
        roles_page.click_edit_for_default_role()
        roles_page.remove_all_permissions_from_default_role()
        Shared(driver).click_submit()

    @then('I see an ultimate end user')
    def i_see_ultimate_end_user_on_page(driver, context):
        destinations_table = ApplicationPage(driver).get_text_of_destinations_table()
        destinations_table_lower = destinations_table.lower()
        assert "name" in destinations_table_lower
        assert "destination type" in destinations_table_lower
        assert "type" in destinations_table_lower
        assert "website" in destinations_table_lower
        assert "address" in destinations_table_lower
        assert "country" in destinations_table_lower
        assert "Ultimate End User" in destinations_table
        assert context.ueu_type in destinations_table
        assert context.ueu_name in destinations_table
        assert context.ueu_website in destinations_table
        assert context.ueu_address in destinations_table
        assert context.ueu_country[0] in destinations_table

    @when('I click on view advice')
    def i_click_on_view_advice(driver, context):
        application_page = ApplicationPage(driver)
        application_page.click_view_advice()
