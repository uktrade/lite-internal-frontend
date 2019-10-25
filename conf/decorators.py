from django.http import Http404
from django.utils.functional import wraps

from conf.constants import DEFAULT_QUEUE_ID
from core.services import get_user_permissions


def has_permission(permission: str):
    def decorator(func):
        def inner_decorator(request, *args, **kwargs):
            permissions = get_user_permissions(args[0])

            if permission in permissions:
                return func(request, *args, **kwargs)
            else:
                pass

            raise Http404()

        return wraps(func)(inner_decorator)

    return decorator


def process_queue_params():
    def decorator(func):
        def inner(view_object, *args, **kwargs):
            queue_id = view_object.request.GET.get('queue', DEFAULT_QUEUE_ID)

            kwargs['queue_params'] = '?queue=' + str(queue_id)

            return func(view_object, *args, **kwargs)

        return inner

    return decorator
