from pytest import fixture

from helpers.utils import get_lite_client


@fixture(scope='session')
def add_an_ecju_query_picklist(context):
    return get_lite_client(context).add_ecju_query_picklist()


@fixture(scope='session')
def add_a_proviso_picklist(context):
    return get_lite_client(context).add_proviso_picklist()


@fixture(scope='session')
def add_a_standard_advice_picklist(context):
    return get_lite_client(context).add_standard_advice_picklist()


@fixture(scope='session')
def add_a_report_summary_picklist(context):
    return get_lite_client(context).add_report_summary_picklist()
