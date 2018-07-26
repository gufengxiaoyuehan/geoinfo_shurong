import timeit
from functools import wraps
from flask import g
from .errors import forbidden, bad_request
from flask import request


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args,**kwargs):
            if not g.current_user.can(permission):
                return forbidden("Insufficient permission")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

