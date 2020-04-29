import os
from django.conf import settings
from pytest_bdd import given, when, then, parsers

from pages.goods_queries_pages import GoodsQueriesPages  # noqa
from pages.organisation_page import OrganisationPage

from ui_automation_tests.fixtures.env import environment  # noqa
from ui_automation_tests.fixtures.add_a_flag import (  # noqa
    add_case_flag,
    add_good_flag,
    add_organisation_flag,
    add_destination_flag,
)
from ui_automation_tests.fixtures.add_queue import add_queue  # noqa
from ui_automation_tests.fixtures.add_a_document_template import (  # noqa
    add_a_document_template,
    get_template_id,
)
from ui_automation_tests.fixtures.add_a_picklist import (  # noqa
    add_a_letter_paragraph_picklist,
    add_an_ecju_query_picklist,
    add_a_proviso_picklist,
    add_a_standard_advice_picklist,
    add_a_report_summary_picklist,
)
from ui_automation_tests.pages.generate_document_page import GeneratedDocument
from ui_automation_tests.pages.give_advice_pages import GiveAdvicePages
from ui_automation_tests.shared.fixtures.apply_for_application import *  # noqa
from ui_automation_tests.shared.fixtures.driver import driver  # noqa
from ui_automation_tests.shared.fixtures.sso_sign_in import sso_sign_in  # noqa
from ui_automation_tests.shared.fixtures.core import (  # noqa
    context,
    api_test_client,
    exporter_info,
    internal_info,
    api_client,
)
from ui_automation_tests.shared.fixtures.urls import internal_url, sso_sign_in_url, api_url  # noqa

import shared.tools.helpers as utils
from pages.assign_flags_to_case import CaseFlagsPages
from pages.shared import Shared
from pages.case_list_page import CaseListPage
from pages.application_page import ApplicationPage
from pages.queues_pages import QueuesPages

from ui_automation_tests.shared.tools.helpers import paginated_item_exists, get_formatted_date_time_m_d_h_s


def pytest_addoption(parser):
    settings.configure(
        DIRECTORY_SSO_API_CLIENT_API_KEY=os.environ.get("DIRECTORY_SSO_API_CLIENT_API_KEY"),
        DIRECTORY_SSO_API_CLIENT_BASE_URL=os.environ.get("DIRECTORY_SSO_API_CLIENT_BASE_URL"),
        DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT=30,
        DIRECTORY_SSO_API_CLIENT_SENDER_ID="directory",
    )
    env = str(os.environ.get("ENVIRONMENT"))
    if env == "None":
        env = "dev"

    parser.addoption("--driver", action="store", default="chrome", help="Type in browser type")
    parser.addoption(
        "--sso_sign_in_url", action="store", default=str(os.environ.get("AUTHBROKER_URL")) + "/login", help="url"
    )

    if env.lower() == "local":
        parser.addoption(
            "--internal_url", action="store", default="http://localhost:" + str(os.environ.get("PORT")), help="url"
        )

        # Get LITE API URL.
        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)
        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )

    elif env == "demo":
        raise NotImplementedError("This is the demo environment - Try another environment instead")
    else:
        parser.addoption(
            "--internal_url",
            action="store",
            default="https://internal.lite.service." + env + ".uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--lite_api_url",
            action="store",
            default="https://lite-api-" + env + ".london.cloudapps.digital/",
            help="url",
        )


# Create driver and url command line adoption
def pytest_exception_interact(node, report):
    if node and report.failed:
        class_name = node._nodeid.replace(".py::", "_class_")
        name = " {0}_{1}".format(class_name, "error")
        try:
            utils.save_screenshot(node.funcargs.get("driver"), name)
        except Exception:  # noqa
            pass


@when("I go to the case")  # noqa
def i_go_to_the_case(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.case_id)


@when("I go to the internal homepage")  # noqa
def when_go_to_internal_homepage(driver, internal_url):  # noqa
    driver.get(internal_url)


@given("I go to internal homepage")  # noqa
def go_to_internal_homepage(driver, internal_url):  # noqa
    driver.get(internal_url)


@given("I sign in to SSO or am signed into SSO")  # noqa
def sign_into_sso(driver, sso_sign_in):  # noqa
    pass


@when("I go to application previously created")  # noqa
def click_on_created_application(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.case_id)


@when("I go to open application previously created")  # noqa
def click_on_created_application(driver, context, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/cases/" + context.case_id)


@given("I create standard application or standard application has been previously created")  # noqa
def create_app(driver, apply_for_standard_application):  # noqa
    pass


@given("I create open application or open application has been previously created")  # noqa
def create_open_app(driver, apply_for_open_application):  # noqa
    pass


@when("I click continue")  # noqa
def i_click_continue(driver):  # noqa
    Shared(driver).click_submit()


@when("I go to flags")  # noqa
def go_to_flags(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/flags/")


@when("I click progress application")  # noqa
def click_post_note(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_progress_application()


@when(parsers.parse('I select status "{status}" and save'))  # noqa
def select_status_save(driver, status, context):  # noqa
    application_page = ApplicationPage(driver)
    application_page.select_status(status)
    context.status = status
    context.date_time_of_update = utils.get_formatted_date_time_h_m_pm_d_m_y()
    Shared(driver).click_submit()


@when("I click on new queue in dropdown")  # noqa
@when("I click on edited queue in dropdown")  # noqa
def queue_shown_in_dropdown(driver, context):  # noqa
    CaseListPage(driver).click_on_queue_name(context.queue_name)


@when(parsers.parse('I click on the "{queue_name}" queue in dropdown'))  # noqa
def system_queue_shown_in_dropdown(driver, queue_name):  # noqa
    CaseListPage(driver).click_on_queue_name(queue_name)


@when("I go to queues")  # noqa
def go_to_queues(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/manage/")


@when("I add case to newly created queue")  # noqa
def move_case_to_new_queue(driver, context):  # noqa
    ApplicationPage(driver).click_move_case_button()
    if not driver.find_element_by_id(context.queue_name).is_selected():
        driver.find_element_by_id(context.queue_name).click()
    Shared(driver).click_submit()


@when("I select previously created flag")  # noqa
def assign_flags_to_case(driver, context):  # noqa
    case_flags_pages = CaseFlagsPages(driver)
    case_flags_pages.select_flag(context.flag_name)
    shared = Shared(driver)
    shared.click_submit()


@given("I create report summary picklist")  # noqa
def add_report_summary_picklist(add_a_report_summary_picklist):  # noqa
    pass


@then("I see the added flags on the queue")  # noqa
def added_flags_on_queue(driver, context):  # noqa
    case_row = driver.find_element_by_id(context.case_id)
    if "(3 of " in case_row.text:
        ApplicationPage(driver).click_expand_flags(context.case_id)
    assert context.flag_name in case_row.text


@then("I see previously created application")  # noqa
def see_queue_in_queue_list(driver, context):  # noqa
    assert QueuesPages(driver).is_case_on_the_list(context.case_id) == 1, (
        "previously created application is not displayed " + context.case_id
    )


@when("I go to the organisation which submitted the case")  # noqa
def go_to_the_organisation_which_submitted_the_case(driver):  # noqa
    ApplicationPage(driver).go_to_organisation()


@when("I click the edit flags link")  # noqa
def go_to_edit_flags(driver):  # noqa
    OrganisationPage(driver).click_edit_organisation_flags()


@when("I show filters")  # noqa
def i_show_filters(driver, context):  # noqa
    CaseListPage(driver).click_show_filters_link()


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@when(  # noqa
    parsers.parse(
        'I respond "{controlled}", "{control_list_entry}", "{report}", "{comment}" and click continue'
    )  # noqa
)  # noqa
def enter_response(driver, controlled, control_list_entry, report, comment):  # noqa
    clc_query_page = GoodsQueriesPages(driver)
    clc_query_page.click_is_good_controlled(controlled)
    clc_query_page.type_in_to_control_list_entry(control_list_entry)
    clc_query_page.choose_report_summary(report)
    clc_query_page.enter_a_comment(controlled)
    Shared(driver).click_submit()


@then("the status has been changed in the application")  # noqa
def status_has_been_changed_in_header(driver, context, internal_info):  # noqa
    application_page = ApplicationPage(driver)
    if context.status.lower() == "under review":
        assert (
            "Under review" in application_page.get_text_of_audit_trail()
        ), "status has not been shown as approved in audit trail"
    elif context.status.lower() == "withdrawn":
        assert (
            context.status in application_page.get_text_of_audit_trail()
        ), "status has not been shown as approved in audit trail"
    elif context.status.lower() == "pv grading review":
        assert (
            context.status in application_page.get_text_of_audit_trail()
        ), "status has not been shown as approved in audit trail"
    elif context.status.lower() == "clc review":
        assert (
            context.status in application_page.get_text_of_audit_trail()
        ), "status has not been shown as approved in audit trail"
    else:
        assert (
            context.status.lower() in application_page.get_text_of_audit_trail()
        ), "status has not been shown as approved in audit trail"

    assert utils.search_for_correct_date_regex_in_element(
        application_page.get_text_of_activity_dates(0)
    ), "date is not displayed after status change"
    # assert (
    #     application_page.get_text_of_activity_users(0) == internal_info["name"]
    # ), "user who has made the status change has not been displayed correctly"


@given("I create a clc query")  # noqa
def create_clc_query(driver, apply_for_clc_query, context):  # noqa
    pass


@when(parsers.parse('filter status has been changed to "{status}"'))  # noqa
def filter_status_change(driver, context, status):  # noqa
    CaseListPage(driver).select_filter_status_from_dropdown(status)
    CaseListPage(driver).click_apply_filters_button()


@when(parsers.parse('I change the user filter to "{status}"'))  # noqa
def filter_status_change(driver, context, status):  # noqa
    CaseListPage(driver).select_filter_user_status_from_dropdown(status)
    CaseListPage(driver).click_apply_filters_button()


@when("I go to the case list page")  # noqa
def case_list_page(driver, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/queues/00000000-0000-0000-0000-000000000001/")


@then("I should see my case in the cases list")  # noqa
def case_in_cases_list(driver, context):  # noqa
    assert paginated_item_exists(context.case_id, driver)
    context.case_row = CaseListPage(driver).get_case_row(context.case_id)
    assert context.reference_code in context.case_row.text


@then("I should see my case SLA")  # noqa
def case_sla(driver, context):  # noqa
    assert CaseListPage(driver).get_case_row_sla(context.case_row) == "0"


@then("I see the case page")  # noqa
def i_see_the_case_page(driver, context):  # noqa
    assert driver.find_element_by_id(ApplicationPage.HEADING_ID).text == context.reference_code


@when("I go to users")  # noqa
def go_to_users(driver, sso_sign_in, internal_url):  # noqa
    driver.get(internal_url.rstrip("/") + "/users/")


@given("an Exhibition Clearance is created")  # noqa
def an_exhibition_clearance_is_created(driver, apply_for_exhibition_clearance):  # noqa
    pass


@when("I combine all advice")  # noqa
def combine_all_advice(driver):  # noqa
    GiveAdvicePages(driver).combine_advice()


@when("I finalise the advice")  # noqa
def finalise(driver):  # noqa
    GiveAdvicePages(driver).finalise()


@when("I select the template previously created")  # noqa
def selected_created_template(driver, context):  # noqa
    GeneratedDocument(driver).click_letter_template(context.document_template_id)
    Shared(driver).click_submit()


@when("I click on the Documents button")  # noqa
def click_documents(driver):  # noqa
    application_page = ApplicationPage(driver)
    application_page.click_documents_button()


@when("I add a flag at level Case")  # noqa
def add_a_case_flag(driver, add_case_flag):  # noqa
    pass


@when("I add a flag at level Good")  # noqa
def add_a_flag(driver, add_good_flag):  # noqa
    pass


@when("I add a flag at level Destination")  # noqa
def add_a_flag(driver, add_destination_flag):  # noqa
    pass


@when("I add a flag at level Organisation")  # noqa
def add_a_flag(driver, add_organisation_flag):  # noqa
    pass


@given("a new queue has been created")  # noqa
def create_queue(context, api_test_client):  # noqa
    api_test_client.queues.add_queue("queue" + get_formatted_date_time_m_d_h_s())
    context.queue_name = api_test_client.context["queue_name"]
    context.queue_id = api_test_client.context["queue_id"]


@given(parsers.parse('I "{decision}" all elements of the application at user and team level'))
def approve_application_objects(context, api_test_client, decision):
    context.advice_type = decision
    text = "abc"
    note = ""
    data = [
        {"type": context.advice_type, "text": text, "note": note, "end_user": context.end_user["id"]},
        {"type": context.advice_type, "text": text, "note": note, "consignee": context.consignee["id"]},
        {"type": context.advice_type, "text": text, "note": note, "good": context.good_id},
    ]

    api_test_client.cases.create_user_advice(context.case_id, data)
    api_test_client.cases.create_team_advice(context.case_id, data)


@given("A template exists for the appropriate decision")
def template_with_decision(context, api_test_client):
    document_template = api_test_client.document_templates.add_template(
        api_test_client.picklists, advice_type=[context.advice_type]
    )
    context.document_template_id = document_template["id"]
    context.document_template_name = document_template["name"]


@when("I go to the final advice page by url")
def final_advice_page(driver, context, internal_url):
    driver.get(
        internal_url.rstrip("/")
        + "/queues/00000000-0000-0000-0000-000000000001/cases/"
        + context.case_id
        + "/final-advice-view/"
    )


@when("I click edit flags link")
def click_edit_case_flags_link(driver):
    ApplicationPage(driver).click_edit_case_flags()


@then("The previously created flag is assigned to the case")
def assert_flag_is_assigned(driver, context):
    assert Shared(driver).is_flag_applied(context.flag_name)
