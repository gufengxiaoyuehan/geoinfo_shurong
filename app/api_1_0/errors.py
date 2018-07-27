import traceback
from flask import jsonify
from . import api
from .exceptions import ValidationError
from ..email import send_mail


def bad_request(message):
    response = jsonify({"error":"bad request", "message":message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({"error": "unauthorized", "message": message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({"error":"forbidden", "message":message})
    response.status_code = 403
    return response


def notfound(message):
    response = jsonify({"error":"not found", "message":message})
    response.status_code = 404
    return response


def internal_server_error(message):
    response = jsonify({"error": "internal error", "message": message})
    response.status_code = 500
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])


## return 400 when exception happend
@api.errorhandler(Exception)
def other_error(e):
    send_mail("gufengxiaoyuehan@163.com","error feedback","email/error_feedback",error=traceback.format_exc())
    return bad_request(e.args[0])

