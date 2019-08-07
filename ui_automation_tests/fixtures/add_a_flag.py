import os

from pytest import fixture
from pytest_bdd import given, when, then, parsers

from fixtures.core import context, driver, sso_login_info, invalid_username, new_cases_queue_id
from fixtures.urls import internal_url, sso_sign_in_url, api_url
from fixtures.apply_for_application import apply_for_standard_application, apply_for_clc_query
from fixtures.sign_in_to_sso import sign_in_to_internal_sso

import helpers.helpers as utils
from pages.flags_pages import FlagsPages
from pages.shared import Shared


@fixture(scope="session")
def add_uae_flag(driver, request, api_url, context):
    flags_page = FlagsPages(driver)
    flags_page.click_add_a_flag_button()
    extra_string = str(utils.get_formatted_date_time_d_h_m_s())
    context.flag_name = "UAE" + extra_string
    flags_page.enter_flag_name(context.flag_name)
    flags_page.select_flag_level("Case")
    Shared(driver).click_submit()
    assert context.flag_name in Shared(driver).get_text_of_table()
