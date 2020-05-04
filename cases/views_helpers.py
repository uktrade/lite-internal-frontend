from conf.constants import Permission, APPLICATION_CASE_TYPES, CLEARANCE_CASE_TYPES, AdviceType


def _check_user_permitted_to_give_final_advice(case_type, permissions):
    """ Check if the user is permitted to give final advice on the case based on their
    permissions and the case type. """
    if case_type in APPLICATION_CASE_TYPES and Permission.MANAGE_LICENCE_FINAL_ADVICE.value in permissions:
        return True
    elif case_type in CLEARANCE_CASE_TYPES and Permission.MANAGE_CLEARANCE_FINAL_ADVICE.value in permissions:
        return True
    else:
        return False


def _can_advice_be_finalised(case):
    """Check that there is no conflicting advice and that the advice can be finalised. """
    items = [*case.goods, *case.destinations]

    for item in items:
        for advice in item.get("advice", []):
            if advice["type"]["key"] == AdviceType.CONFLICTING:
                return False
    return True


def _can_user_create_and_edit_advice(case, permissions):
    """Check that the user can create and edit advice. """
    return Permission.MANAGE_TEAM_CONFIRM_OWN_ADVICE.value in permissions or (
        Permission.MANAGE_TEAM_ADVICE.value in permissions and not case.get("has_advice").get("my_user")
    )
