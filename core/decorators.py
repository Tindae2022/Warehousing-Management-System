from django.core.exceptions import PermissionDenied
from functools import wraps


def user_is_sales_manager(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_sales_manager():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_warehouse_manager(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_warehouse_manager():
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap


def user_is_customer(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user

        if user.is_authenticated and user.is_customer():
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    return wrap
