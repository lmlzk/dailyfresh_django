from django.shortcuts import redirect
from functools import wraps


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *view_args, **view_kwargs):
        if request.session.has_key('is_login'):
            return view_func(request, *view_args, **view_kwargs)
        else:
            return redirect('/user/login/')
    return wrapper
