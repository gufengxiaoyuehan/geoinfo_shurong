from . import api
from .. import db
from flask import jsonify,request,url_for,current_app
from ..models import Permission,Info,User,Coordinate
from .decorators import permission_required
from .errors import forbidden, bad_request, notfound
from .exceptions import ValidationError
from .utils import paginate


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


@api.route("/user/<userid>/infos/")
@permission_required(Permission.GET_POST)
def get_user(userid):
    user = User.query.get(userid)
    if not user:
        return notfound("user doesnot exists")
    print(user.properties.all())
    infos = [properties.info for properties in user.properties.all()]
    amount = request.args.get("amount", 15, type=int)
    page = request.args.get("page", 1, type=int)
    infos = sorted(
        [{"_id": info.id, "properties": info.properties.to_json(), "coordinate": info.coordinate.to_json()} for
         info_ in infos for info in info_], key=lambda x: x.get("_id"))
    total= len(infos)
    page, prev, next = paginate(total,page,amount,"api.get_user",userid=userid,_external=True)
    return jsonify({
        "infos": infos[(page-1)*amount:page**amount],
        "prev": prev,
        "next": next,
        "total":total
    })


@api.route("/nearby/<coordiante>")
@permission_required(Permission.GET_POST)
def get_nearby(coordiante):
    print(coordiante)
    try:
        x,y = map(float,coordiante.split(","))
        if x > 180 or x < 0:
            raise ValidationError("latitude provide not legal")
        if y > 180 or y < 0:
            raise ValidationError("longitude provide not legal")
    except ValueError as e:
        raise ValidationError("coordinate <x,y> provided not available")

    distance = abs(request.args.get("distance",0.01, type=float))
    coordinates = Coordinate.query.filter(Coordinate.distance_nearby(x,y,distance))

    infos = [ coordinate.info for coordinate in coordinates]
    amount = request.args.get("amount",15,type=int)
    page = request.args.get("page",1,type=int)
    infos = sorted([{"_id": info.id, "properties": info.properties.to_json(), "coordinate": info.coordinate.to_json()} for
                  info_ in infos for info in info_], key=lambda x: x.get("_id"))
    total = len(infos)
    page, prev, next = paginate(total, page, amount, "api.get_nearby", coordiante=coordiante, _external=True)
    print((page-1)*amount)
    return jsonify({
        "infos": infos[(page-1)*amount:page*amount],
        "prev":prev,
        "next":next,
        "total":total
    })