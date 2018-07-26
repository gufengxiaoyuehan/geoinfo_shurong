from . import api
from .. import db
from flask import jsonify,request,g,url_for,current_app
from ..models import Permission,Info,Coordinate,Properties
from .decorators import permission_required
from .errors import forbidden,bad_request


@api.route("/infos/", methods=["POST"])
@permission_required(Permission.PUT_POST)
def new_info():
    cl = request.content_length
    max_length = current_app.config.get("REQUEST_MAX_LENGTH", 3)
    if cl is not None and cl > max_length * 1024 * 1024:
        return bad_request("POST SIZE exceeds max-size")
    info = Info.from_json(request.json)
    db.session.add(info)
    db.session.commit()
    return jsonify({"success":"true","info":info.id}),201


@api.route("/infos/", methods = ["GET"])
@permission_required(Permission.GET_POST)
def get_infos():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("amount",15,type=int)
    pagination = Info.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    infos = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for("api.get_infos",page=page-1,amount=per_page,_external=True)
    next = None
    if pagination.has_next:
        next = url_for("api.get_infos", page=page+1,amount=per_page,_external=True)
    return jsonify({
        "infos":[{"_id": info.id, "properties": info.properties.to_json(),"coordinate": info.coordinate.to_json()} for info in infos],
        "prev":prev,
        "next":next,
        "count":pagination.total
    })