from functools import wraps
from django.conf import settings
from django.contrib.auth import get_user
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils.decorators import available_attrs, method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View


def require_authenticated_permission(permission):

    def decorator(cls):
        if (not isinstance(cls, type) or not issubclass(cls, View)):
            raise ImproperlyConfigured(
                "require authenticated permission must be"
                " applied to subclass of View class.")
        check_auth = method_decorator(login_required)
        check_perm = method_decorator(
            permission_required(
                permission, raise_exception = True))
        cls.dispatch = check_auth(check_perm(cls.dispatch))
        return cls
    return decorator

# Has no purpose whatsoever

def custom_login_required(view):
    # @wraps(view, assigned = available_attrs(view))
    # def new_view(request, *args, **kwargs):
    #     user = get_user(request)
    #     if user.is_authenticated():
    #         return view(request, *args, **kwargs)
    #     else:
    #         url = '{}?next={}'.format(
    #             settings.LOGIN_URL,
    #             request.path)
    #         return redirect(url)
    # return new_view

    decorator = method_decorator(login_required)
    decorated_view = decorator(view)
    return decorated_view

def class_login_required(cls):
    if (not isinstance(cls, type) or not issubclass(cls, View)):
        raise ImproperlyConfigured(
            "class_login_required must be applied to"
            "subclass of View class.")
    decorator = method_decorator(login_required)
    cls.dispatch = decorator(cls.dispatch)
    return cls

def require_authenticated_permission2(permission):

    def decorator(view):
        check_auth = method_decorator(login_required)
        check_perm = method_decorator((
            permission_required(
                permission, raise_exception = True)))
        decorated_view = (
            check_auth(check_perm(view)))
        return decorated_view

    return decorator
