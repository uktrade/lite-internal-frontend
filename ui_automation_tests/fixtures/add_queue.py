from pytest import fixture
import shared.tools.helpers as utils
from pages.queues_pages import QueuesPages
from pages.shared import Shared


@fixture(scope="module")
def add_queue(driver, request, api_url, context):
    QueuesPages(driver).click_add_a_queue_button()
    extra_string = str(utils.get_formatted_date_time_y_m_d_h_s())
    context.queue_name = "z " + extra_string
    QueuesPages(driver).enter_queue_name(context.queue_name)
    Shared(driver).click_submit()
