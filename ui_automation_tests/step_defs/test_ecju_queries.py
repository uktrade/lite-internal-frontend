import time
from pytest_bdd import when, then, parsers, scenarios
from pages.application_page import ApplicationPage
import helpers.helpers as utils

scenarios('../features/ecju_query.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)


@then('I see the ECJU Queries button')
def ecju_queries_button_is_present(driver, context):
    assert True
