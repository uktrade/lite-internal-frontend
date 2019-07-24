from conf.settings import env
import os
from selenium import webdriver
from pytest import fixture


@fixture(scope="session", autouse=True)
def driver(request):
    browser = request.config.getoption("--driver")
    if browser == 'chrome':
        if str(os.environ.get('ENVIRONMENT')) == 'None':
            browser = webdriver.Chrome("chromedriver")
        else:
            browser = webdriver.Chrome()
        browser.get("about:blank")
        browser.implicitly_wait(3)
        return browser
    else:
        print('only chrome is supported at the moment')

    def fin():
        driver.quit()
        request.addfinalizer(fin)


@fixture(scope="session")
def context():
    class Context(object):
        pass

    return Context()


@fixture(scope="session")
def sso_login_info():
    sso_email = env('TEST_SSO_EMAIL')
    sso_password = env('TEST_SSO_PASSWORD')

    return {'email': sso_email, 'password': sso_password}
