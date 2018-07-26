from datetime import datetime

from flask import current_app
from math import sqrt

from sqlalchemy import and_
from sqlalchemy.ext.hybrid import hybrid_method
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from . import db
from .exceptions import ValidationError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


class Permission:
    GET_POST = 0x01
    PUT_POST = 0x02


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")
    permission = db.Column(db.Integer,default=0)

    def __repr__(self):
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    properties = db.relationship("Properties", backref="user",lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data["id"])

    def generate_auth_token(self,expiration):
        s = Serializer(current_app.config["SECRET_KEY"],expires_in=expiration)
        return s.dumps({"id":self.id})

    def can(self,permission):
        return self.role is not None and (self.role.permission & permission) == permission

    def __repr__(self):
        return "<User %r>" % self.username


class Properties(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    text_info = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source =db.Column(db.String(50))
    sentiment = db.Column(db.String(50))
    sentiStrings = db.Column(db.String(50))
    labelledSentiment =db.Column(db.String(50))
    crowder = db.Column(db.String(50))
    info = db.relationship("Info", backref="properties", lazy="dynamic")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def to_json(self):
        property_json = {
            "text":self.text_info,
            "userID": self.user.id,
            "userName":self.user.username,
            "day": self.timestamp.day,
            "month": self.timestamp.month,
            "year": self.timestamp.year,
            "hour": self.timestamp.hour,
            "minute": self.timestamp.minute,
            "second": self.timestamp.second,
            "source": self.source,
            "sentiment": self.sentiment,
            "sentiString": self.sentiStrings,
            "labelledSentiment": self.labelledSentiment,
            "crowder": self.crowder
        }
        return property_json

    @classmethod
    def from_json(cls,json_properties):
        try:
            timestamp = datetime(
                year=int(json_properties.get("year")),
                month=int(json_properties.get("month")),
                day=int(json_properties.get("day")),
                hour=int(json_properties.get("hour")),
                minute=int(json_properties.get("minute")),
                second=int(json_properties.get("second"))
            )
            text = json_properties.get("text")
            if not text:
                raise ValidationError("text must be supplied")
            source = json_properties.get("source")
            sentiment = json_properties.get("sentiment")
            sentiStrings = json_properties.get("sentiStrings")
            labelledSentiment = json_properties.get("labelledSentiment")
            crowder = json_properties.get("crowder")

            user = User.query.get(json_properties.get("userID"))
            # create new user
            if not user:
                username = json_properties.get("userName")
                if username:
                    user = User(username=username,id=json_properties.get("userID"))
            return cls(text_info=text,user=user,timestamp=timestamp,source=source,sentiment=sentiment
                ,sentiStrings=sentiStrings,labelledSentiment=labelledSentiment,crowder=crowder
            )
        except (TypeError,ValueError) as e:
            raise ValidationError(e.args[0])

    def __repr__(self):
        return "<Properties %r>" % self.id


class Coordinate(db.Model):
    __tablename__ = "coordinates"
    id = db.Column(db.Integer, primary_key=True)
    shape = db.Column(db.String(12))
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    info = db.relationship("Info", backref="coordinate", lazy="dynamic")

    @hybrid_method
    def distance_nearby(self,x,y, distance):
        return self.x.between(x-distance,x+distance) and self.y.between(y-distance,y+distance)

    @distance_nearby.expression
    def distance_nearby(cls, x, y , distance):
        return and_(cls.x.between(x-distance,x+distance) , cls.y.between(y-distance,y+distance))

    @validates("x")
    def validate_x(self,key, x):
        if x > 180 or x < 0:
            raise ValidationError("coordinate x out of range")
        return x

    @validates("y")
    def validate_y(self,key,y):
        if y > 180 or y < 0:
            raise ValidationError("coordinate x out range")
        return y

    @classmethod
    def from_json(cls,json_coordinate):
        try:
            shape = json_coordinate.get("type")
            x,y = json_coordinate.get("coordinates")
        except TypeError as e:
            raise ValidationError(e.args[0])
        return cls(shape=shape,x=x,y=y)

    def to_json(self):
        coordinate_json = {
            "type":self.shape,
            "coordinates":[self.x, self.y]
        }
        return coordinate_json


class Info(db.Model):
    __tablename__ = "infos"
    id = db.Column(db.String(50),primary_key=True)
    properties_id = db.Column(db.Integer,db.ForeignKey("properties.id"))
    coordinate_id = db.Column(db.Integer, db.ForeignKey("coordinates.id"))

    @classmethod
    def from_json(cls,json_info):
        coordinate = Coordinate.from_json(json_info.get("coordinate"))
        properties = Properties.from_json(json_info.get("properties"))
        return cls(id=json_info.get("_id"), properties=properties, coordinate=coordinate)

    def to_json(self):
        info_json = {
            "id" : self.id,
            "properties": self.properties.to_json(),
            "coordinate": self.coordinate.to_json()
        }
        return info_json

    def __repr__(self):
        return "<Info %r>" % self.id