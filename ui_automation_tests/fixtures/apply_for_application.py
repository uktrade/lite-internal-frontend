from pytest import fixture
import datetime
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="module")
def apply_for_standard_application(driver, request, context):
    timer = Timer()
    api = get_or_create_attr(context, 'api', lambda: SeedData(logging=True))

    app_time_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context.app_time_id = app_time_id

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
            "name": "Individual",
            "address": "Bullring, Birmingham SW1A 0AA",
            "country": "GB",
            "type": "commercial",
            "website": "https://www.anothergov.uk"
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
