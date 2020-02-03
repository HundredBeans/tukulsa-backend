from blueprints import db
from flask_restful import fields
from datetime import datetime


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id_api = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(1000), default=None)


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    trx_id_api = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    provider = db.Column(db.String(10), nullable=False, default=None)
    phone_number = db.Column(db.String(13), nullable=False)
    label = db.Column(db.String(255), nullable=False, default=None)
    nominal = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    payment_status = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    trx_product = db.relationship('product', backref='transactions')
    trx_timedetail = db.relationship('timedetails', backref='transactions')


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
