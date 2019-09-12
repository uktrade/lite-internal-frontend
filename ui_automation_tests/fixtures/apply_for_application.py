from pytest import fixture
import datetime
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr

from helpers.wait import wait_for_ultimate_end_user_document, wait_for_end_user_document


@fixture(scope="module")
def apply_for_standard_application(driver, request, api_url, context):
    timer = Timer()
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))

    app_time_id = datetime.datetime.now().strftime(" %d%H%M%S")
    context.app_time_id = app_time_id
    context.ueu_type = "commercial"
    context.ueu_name = "Individual"
    context.ueu_website = "https://www.anothergov.uk"
    context.ueu_address = "Bullring, Birmingham SW1A 0AA"
    context.ueu_country = ["GB", "United Kingdom"]

    draft_id, ultimate_end_user_id = api.add_draft(
        draft={
            "name": "Test Application " + app_time_id,
            "licence_type": "standard_licence",
            "export_type": "permanent",
            "have_you_been_informed": "yes",
            "reference_number_on_information_form": "1234"}, 
        good={
            "good_id": "",
            "quantity": 1234,
            "unit": "MTR",
            "value": 1},
        enduser={
            "name": "Mr Smith",
            "address": "London",
            "country": "UA",
            "sub_type": "government",
            "website": "https://www.smith.com"
        },
        ultimate_end_user={
            "name": context.ueu_name,
            "address": context.ueu_address,
            "country": context.ueu_country[0],
            "sub_type": context.ueu_type,
            "website": context.ueu_website
        },
        consignee={
            "name": "Government",
            "address": "Westminster, London SW1A 0BB",
            "country": "GB",
            "sub_type": "government",
            "website": "https://www.gov.uk"
        },
        third_party={
            "name": "Individual",
            "address": "Ukraine, 01532",
            "country": "UA",
            "sub_type": "agent",
            "website": "https://www.anothergov.uk"
        }
    )
    document_is_processed = wait_for_end_user_document(api=api, draft_id=draft_id)
    assert document_is_processed, "Document wasn't successfully processed"
    ultimate_end_user_document_is_processed = wait_for_ultimate_end_user_document(
        api=api, draft_id=draft_id, ultimate_end_user_id=ultimate_end_user_id)
    assert ultimate_end_user_document_is_processed, "Ultimate end user document wasn't successfully processed"
    api.submit_application()
    context.app_id = api.context['application_id']
    context.case_id = api.context['case_id']
    context.consignee = api.context['consignee']
    context.third_party = api.context['third_party']
    timer.print_time('apply_for_standard_application')


@fixture(scope="module")
def apply_for_clc_query(driver, request, api_url, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    api.add_clc_query()
    context.case_id = api.context['case_id']
