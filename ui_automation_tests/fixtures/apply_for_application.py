from pytest import fixture
import datetime
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="module")
def apply_for_standard_application(driver, request, context):
    timer = Timer()
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))

    app_time_id = datetime.datetime.now().strftime(" %H:%M:%S")
    context.app_time_id = app_time_id
    context.ueu_type = "commercial"
    context.ueu_name = "Individual"
    context.ueu_website = "https://www.anothergov.uk"
    context.ueu_address = "Bullring, Birmingham SW1A 0AA"
    context.ueu_country = ["GB", "United Kingdom"]

    api.add_draft(
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
            "type": "government",
            "website": "https://www.smith.com"
        },
        ultimate_end_user={
            "name": context.ueu_name,
            "address": context.ueu_address,
            "country": context.ueu_country[0],
            "type": context.ueu_type,
            "website": context.ueu_website
        }
    )
    api.submit_application()
    context.app_id = api.context['application_id']
    context.case_id = api.context['case_id']
    timer.print_time('apply_for_standard_application')


@fixture(scope="module")
def apply_for_clc_query(driver, request, context):
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))
    api.add_clc_query()
    context.case_id = api.context['case_id']
