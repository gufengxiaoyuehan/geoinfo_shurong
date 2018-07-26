from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify
from .errors import forbidden, unauthorized
from . import api
from ..models import User
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(name_or_token, password):
    if name_or_token == "":
        return False
    if password == "":
        g.current_user = User.verify_auth_token(name_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=name_or_token).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized("Invalid credentials")


@api.before_request
@auth.login_required
def before_request():
    pass


@api.route("/tokens/", methods=["GET"])
def get_token():
    if g.get("token_used"):
        return unauthorized("token has used")
    return jsonify({"token": g.current_user.generate_auth_token(expiration=3600).decode(),"expiration":3600})