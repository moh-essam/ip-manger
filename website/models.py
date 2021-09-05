from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy_utils import IPAddressType


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    subnets = db.relationship('Subnet')


class IPAddress(db.Model):
    ipad = db.Column(IPAddressType, primary_key=True, unique=True)
    status = db.Column(db.String(150))
    subnet_id = db.Column(db.Integer, db.ForeignKey('subnet.id'))


class VlanId(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(150))
    subnet_id = db.Column(db.Integer, db.ForeignKey('subnet.id'))


class Subnet(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150), unique=True)
    vlanId = db.relationship('VlanId')
    mask = db.Column(db.Integer)
    ip_range = db.relationship('IPAddress')
 




