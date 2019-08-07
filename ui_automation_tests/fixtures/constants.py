from pytest import fixture


@fixture(scope="session")
def new_cases_queue_id():
    return "00000000-0000-0000-0000-000000000001"
