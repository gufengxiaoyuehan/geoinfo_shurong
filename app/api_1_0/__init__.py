from flask import Blueprint

api = Blueprint("api",__name__)

from . import authentication,decorators,errors,exceptions,infos