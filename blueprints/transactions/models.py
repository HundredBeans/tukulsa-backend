from blueprints import db
from flask_restful import fields
from datetime import datetime


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    operator = db.Column(db.String(15), nullable=False)
    code = db.Column(db.String(255), unique=True, nullable=False)
    nominal = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    valid_to = db.Column(db.String(5), nullable=False)
    image = db.Column(db.String(255), nullable=False)

    response_fileds = {
        'id': fields.Integer,
        'operator': fields.String,
        'code': fields.String,
        'nominal': fields.String,
        'price': fields.String,
        'valid_to': fields.String,
        'image': fields.String
    }

    def __init__(self, operator, code, nominal, price, valid_to, image):
        self.operator = operator
        self.code = code
        self.nominal = nominal
        self.price = price
        self.valid_to = valid_to
        self.image = image


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    order_id = db.Column(db.String(255), default=None)
    operator = db.Column(db.String(15), nullable=False, default=None)
    label = db.Column(db.String(255), nullable=False, default=None)
    nominal = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    # PENDING PAID EXPIRED FAILED NOTPAID
    payment_status = db.Column(db.String(20), default="NOTPAID")
    # PENDING SUCCESS FAILED PROCESSING
    order_status = db.Column(db.String(20), default="PROCESSING")
    trx_users = db.relationship(
        'Users', backref='transactions', cascade="all", lazy="joined")
    trx_product = db.relationship(
        'Product', backref='transactions', cascade="all", lazy="joined")
    trx_timedetail = db.relationship(
        'Timedetails', backref='transactions', cascade="all", lazy="joined")

    response_fields = {
        "id": fields.Integer,
        "phone_number": fields.String,
        "order_id": fields.String,
        "product_id": fields.String,
        "operator": fields.String,
        "label": fields.String,
        "nominal": fields.Integer,
        "price": fields.Integer,
        "created_at": fields.DateTime,
        "payment_status": fields.String,
        "order_status": fields.String
    }

    def __init__(self, user_id, phone_number, product_id, operator, label, nominal, price, created_at):
        self.user_id = user_id
        self.phone_number = phone_number
        self.product_id = product_id
        self.operator = operator
        self.label = label
        self.nominal = nominal
        self.price = price
        self.created_at = created_at

    
    


class Timedetails(db.Model):
    __tablename__ = "timedetails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_trxid = db.Column(db.Integer, db.ForeignKey(
        'transactions.id', ondelete='CASCADE'), nullable=False)
    time_userid = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False, default=None)
    month = db.Column(db.Integer, nullable=False, default=None)
    date = db.Column(db.Integer, nullable=False, default=None)
    month_char = db.Column(db.String(15), default=None)
    date_char = db.Column(db.String(10), default=None)
