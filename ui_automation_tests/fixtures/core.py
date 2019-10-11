from pytest import fixture
from conf.settings import env
from shared.tools.utils import get_lite_client


@fixture(scope='session')
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope='session')
def sso_login_info(request):
    sso_email = env('TEST_SSO_EMAIL')
    sso_password = env('TEST_SSO_PASSWORD')

    return {'email': sso_email, 'password': sso_password}


@fixture(scope='session')
def sso_users_name():
    sso_name = env('TEST_SSO_NAME')
    return sso_name


@fixture(scope='module')
def invalid_username(request):
    return 'invalid@mail.com'


@fixture(scope='session')
def exporter_info(request):
    exporter_sso_email = env('TEST_EXPORTER_SSO_EMAIL')
    first_name = 'Test'
    last_name = 'Lite'

    return {
        'email': exporter_sso_email,
        'first_name': first_name,
        'last_name': last_name
    }


@fixture(scope='session')
def internal_info(request):
    gov_user_email = env('TEST_SSO_EMAIL')
    gov_user_first_name, gov_user_last_name = env('TEST_SSO_NAME').split(' ')

    return {
        'email': gov_user_email,
        'first_name': gov_user_first_name,
        'last_name': gov_user_last_name
    }


@fixture(scope='session')
def seed_data_config(request, exporter_info, internal_info, s3_key):
    api_url = request.config.getoption('--lite_api_url')
    return {
        'api_url': api_url,
        'exporter': exporter_info,
        'gov': internal_info,
        's3_key': s3_key
    }


def clear_down(context, seed_data_config):
    lite_client = get_lite_client(context, seed_data_config)
    if 'Application Bin' not in str(lite_client.get_queues()):
        lite_client.add_queue('Application Bin')
        bin_id = context['queue_id']
    else:
        for queue in lite_client.get_queues():
            if queue['name'] == 'Application Bin':
                bin_id = queue['id']
                break
    lite_client.assign_test_cases_to_bin(bin_id)


@fixture(scope='session')
def new_cases_queue_id():
    return '00000000-0000-0000-0000-000000000001'


@fixture(scope='session')
def s3_key(request):
    s3_key = env('TEST_S3_KEY')
    return s3_key
