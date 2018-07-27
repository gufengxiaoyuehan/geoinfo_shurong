from flask import request

from . import main
from ..api_1_0.errors import notfound,internal_server_error


@main.app_errorhandler(404)
def page_not_found(e):
    if request.path.startswith("/api/"):
        return notfound("page not found")
    else:
        return e


@main.app_errorhandler(500)
def page_not_found(e):
    if request.path.startswith("/api/"):
        return internal_server_error("internal server error")
    else:
        return e
