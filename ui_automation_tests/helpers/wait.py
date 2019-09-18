import time

# How long in seconds the function should be attempted until giving up
from helpers.helpers import page_is_ready, menu_is_visible

timeout_limit = 20
# How frequently in seconds the function should be checked
function_retry_interval = 1


def wait_for_function(func, **kwargs):
    time_no = 0
    while time_no < timeout_limit:
        if func(**kwargs):
            return True
        time.sleep(function_retry_interval)
        time_no += function_retry_interval
    return False


def wait_for_document(func, draft_id):
    return wait_for_function(func, draft_id=draft_id)


def wait_for_ultimate_end_user_document(func, draft_id, ultimate_end_user_id):
    return wait_for_function(func, draft_id=draft_id,
                             ultimate_end_user_id=ultimate_end_user_id)


def wait_until_page_is_loaded(driver):
    return wait_for_function(page_is_ready, driver=driver)


def wait_until_menu_is_visible(driver):
    return wait_for_function(menu_is_visible, driver=driver)
