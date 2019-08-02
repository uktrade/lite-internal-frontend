from pytest import fixture
import datetime
from pages.add_goods_page import AddGoodPage
from pages.exporter_hub import ExporterHub
from conf.settings import env
import helpers.helpers as utils

from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="session")
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
        }
    )
    api.submit_application()
    context.app_id = api.context['application_id']
    timer.print_time('apply_for_standard_application')


@fixture(scope="session")
def apply_for_clc_query(driver, request, context):
    exporter_hub = ExporterHub(driver)
    driver.get(request.config.getoption("--exporter_url"))
    if "login" in driver.current_url:
        exporter_hub.login(env('TEST_EXPORTER_SSO_EMAIL'),
                           env('TEST_EXPORTER_SSO_PASSWORD'))
    exporter_hub.click_goods_button()
    add_goods_page = AddGoodPage(driver)
    add_goods_page.click_add_a_good()
    exporter_hub = ExporterHub(driver)
    add_goods_page = AddGoodPage(driver)
    date_time = utils.get_current_date_time_string()
    good_description = "%s %s" % ("MPG 2.9", date_time)
    context.good_description = good_description
    add_goods_page.enter_description_of_goods(good_description)
    add_goods_page.select_is_your_good_controlled()
    add_goods_page.enter_control_unsure_details("%s unsure" % "MPG 2.9")
    add_goods_page.select_is_your_good_intended_to_be_incorporated_into_an_end_product()
    exporter_hub.click_save_and_continue()
    add_goods_page.select_control_unsure_confirmation()
    exporter_hub.click_save_and_continue()
    case_id = add_goods_page.assert_good_is_displayed_and_return_case_id(context.good_description)
    context.case_id = case_id
    driver.get(request.config.getoption("--internal_url"))
