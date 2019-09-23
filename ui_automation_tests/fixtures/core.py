import warnings

from conf.settings import env
import os
import types
from selenium import webdriver
from pytest import fixture

from helpers.seed_data import SeedData
from helpers.utils import get_or_create_attr

# set_timeouts are for elements that dont exist that dont need a 10 second timeout to return that they dont exist.
# so wait 0 seconds to return that the element doesnt exist rather than 10.

def set_timeout_to(self, time=0):
    self.implicitly_wait(time)


def set_timeout_to_10_seconds(self):
    self.implicitly_wait(10)


@fixture(scope='session', autouse=True)
def driver(request):
    """
    Open a browser for the session
    """
    browser = request.config.getoption('--driver').lower()

    # Set browser
    if browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()

        if str(os.environ.get('TEST_TYPE_HEADLESS')) == 'True':
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        browser = webdriver.Chrome(options=chrome_options)
    elif browser == 'safari':
        warnings.warn('Safari is buggy, use at your own risk', UserWarning, stacklevel=2)
        browser = webdriver.Safari()
        browser.maximize_window()
    else:
        print('Only Chrome is supported at the moment')

    browser.set_timeout_to = types.MethodType(set_timeout_to, browser)
    browser.set_timeout_to_10_seconds = types.MethodType(set_timeout_to_10_seconds, browser)
    browser.get("about:blank")
    browser.set_timeout_to_10_seconds()
    return browser


@fixture(scope="session")
def context(request):
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def sso_login_info(request):
    sso_email = env('TEST_SSO_EMAIL')
    sso_password = env('TEST_SSO_PASSWORD')

    return {'email': sso_email, 'password': sso_password}


@fixture(scope="session")
def sso_users_name():
    sso_name = env('TEST_SSO_NAME')
    return sso_name


@fixture(scope="module")
def invalid_username(request):
    return "invalid@mail.com"


def clear_down(context, api_url):
    api = get_or_create_attr(context, 'api', lambda: SeedData(api_url=api_url, logging=True))
    print(api.get_queues())
    if "Application Bin" not in str(api.get_queues()):
        api.add_queue("Application Bin")
        bin_id = context['queue_id']
    else:
        for queue in api.get_queues():
            if queue['name'] == "Application Bin":
                bin_id = queue['id']
                break
    api.assign_test_cases_to_bin(bin_id)


@fixture(scope="session")
def new_cases_queue_id():
    return "00000000-0000-0000-0000-000000000001"
