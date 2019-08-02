from pytest import fixture
from helpers.seed_data import SeedData
from helpers.utils import Timer, get_or_create_attr


@fixture(scope="session")
def register_organisation(driver, request, sso_login_info, context):
    timer = Timer()
    get_or_create_attr(context, 'api', lambda: SeedData(logging=False))
    context.org_name = "Test Org"
    context.org_registered_status = True
    timer.print_time('register_organisation')
