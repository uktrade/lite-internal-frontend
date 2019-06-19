from pytest_bdd import scenarios, given, when, then, parsers, scenarios
from pages.header_page import HeaderPage
from pages.shared import Shared
from pages.teams_pages import TeamsPages
import helpers.helpers as utils
from conftest import context

scenarios('../features/users.feature', strict_gherkin=False)

import logging
log = logging.getLogger()
console = logging.StreamHandler()
log.addHandler(console)
