from http import HTTPStatus


def validate_query_type_question(_, json):
    if json.get("ecju_query_type"):
        return json, HTTPStatus.OK

    return (
        {"errors": {"ecju_query_type": ["Select the type of licence or clearance you need"]}},
        HTTPStatus.BAD_REQUEST,)