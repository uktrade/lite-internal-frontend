from pytest import fixture
import shared.tools.helpers as utils


@fixture(scope="module")
def add_case_flag(context, api_test_client):
    if not api_test_client.flags.get_list_of_flags_for_level("Case"):
        api_test_client.flags.add_flag("Case " + utils.get_formatted_date_time_m_d_h_s(), "Case")
    context.case_flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]


@fixture(scope="module")
def add_good_flag(context, api_test_client):
    if not api_test_client.flags.get_list_of_flags_for_level("Good"):
        api_test_client.flags.add_flag("Good " + utils.get_formatted_date_time_m_d_h_s(), "Good")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]


@fixture(scope="module")
def add_destination_flag(context, api_test_client):
    if not api_test_client.flags.get_list_of_flags_for_level("Destination"):
        api_test_client.flags.add_flag("Place " + utils.get_formatted_date_time_m_d_h_s(), "Destination")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]


@fixture(scope="module")
def add_organisation_flag(context, api_test_client):
    if not api_test_client.flags.get_list_of_flags_for_level("Organisation"):
        api_test_client.flags.add_flag("Org " + utils.get_formatted_date_time_m_d_h_s(), "Organisation")
    context.flag_name = api_test_client.context["flag_name"]
    context.flag_id = api_test_client.context["flag_id"]
