from blueprints import db
from flask_restful import fields
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_id = db.Column(db.String(255), nullable=False, unique=True)
    display_name = db.Column(db.String(255), nullable=False)
    user_transactions = db.relationship(
        'Transactions', backref='users', cascade="all, delete", lazy='dynamic')
    user_chat = db.relationship(
        'Chat', backref='users', cascade="all, delete", lazy="joined")

    # balance=db.Column(db.Integer, nullable=True)
    response_fileds = {
        'id': fields.Integer,
        'display_name': fields.String,
        'line_id': fields.String
        # "balance":fields.Integer
    }

    def __init__(self, line_id, display_name, balance):
        self.line_id = line_id
        self.display_name = display_name
        # self.balance=balance


class Chat(db.Model):
    __tablename__ = "chat"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_userid = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    status_number = db.Column(db.Boolean, default=False)
    status_nominal = db.Column(db.Boolean, default=False)
    status_report = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(14), default=None)
    nominal = db.Column(db.Integer, default=None)
    operator = db.Column(db.String(15), default=None)

    response_fileds = {
        'id': fields.Integer,
        'chat_userid': fields.Integer,
        'status_number': fields.Boolean,
        'status_nominal': fields.Boolean,
        'status_report': fields.Boolean,
        'phone_number': fields.String,
        'nominal': fields.Integer,
        'operator': fields.String
    }

    def __init__(self, chat_userid):
        self.chat_userid = chat_userid

class Report(db.Model):
    __tablename__ = "report"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
    'users.id', ondelete='CASCADE'), nullable=False)
    order_id = db.Column(db.String(255), nullable=False, default=None)
    text = db.Column(db.String(1000), default="Report :")
    email = db.Column(db.String(255), default=None)
    security_code = db.Column(db.String(32), default=None)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(255), default="BELUM DISELESAIKAN")

    response_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'order_id': fields.String,
        'text': fields.String,
        'email': fields.String,
        'security_code': fields.String,
        'created_at': fields.DateTime,
        'status': fields.String
    }

    def __init__ (self, user_id, order_id, created_at):
        self.user_id = user_id
        self.order_id = order_id
        self.created_at = created_at