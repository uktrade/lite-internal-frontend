from django.http import Http404
from django.utils.functional import wraps

from conf.constants import Permissions
from core.services import get_user_permissions


def has_permission(permission: str):
    """
    Decorator for views that checks that the user has a given permission
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not getattr(Permissions, permission):
                raise NotImplementedError(f"{permission} is not implemented in core.permissions")

            user_permissions = get_user_permissions(request)

            if permission in user_permissions:
                return view_func(request, *args, **kwargs)

            raise Http404

        return _wrapped_view

    return decorator
