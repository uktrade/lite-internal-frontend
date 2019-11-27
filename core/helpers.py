from django.core.exceptions import PermissionDenied

from conf import decorators
from conf.constants import Permissions
from core.services import get_user_permissions


def convert_dict_to_query_params(dictionary):
    items = []
    for key, value in dictionary.items():
        if isinstance(value, list):
            for val in value:
                items.append(key + "=" + str(val))
        else:
            items.append(key + "=" + str(value))
    return "&".join(items)


def has_permission(request, permission):
    """
    Returns true if the user has a given permission
    """
    if not getattr(Permissions, permission):
        raise NotImplementedError(f"{permission} is not implemented in core.permissions")

    user_permissions = get_user_permissions(request)

    return permission in user_permissions


def _wrap_with_permission(permission, view_func=None):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, redirecting to the login page if necessary.
    """
    actual_decorator = decorators.has_permission(permission)

    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def decorate_patterns_with_permission(patterns, permission: str):
    decorated_patterns = []
    for pattern in patterns:
        callback = pattern.callback
        pattern.callback = _wrap_with_permission(permission, callback)
        pattern._callback = _wrap_with_permission(permission, callback)
        decorated_patterns.append(pattern)
    return decorated_patterns
