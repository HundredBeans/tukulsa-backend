from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from .models import Users
from ..transactions.models import *
from blueprints import db

bp_users = Blueprint('users', __name__)
api = Api(bp_users)

# USER GET SELF TRANSACTION HISTORY
class UserById(Resource):
  def get(self):
    pass

# POST AND GET SELF INFO USER
class UserProfile(Resource):
  def get(self):
    pass
  
  def post(self):
    pass

# USER TOP UP MOBILE BALANCE
class UserTopUp(Resource):
  def post(self):
    pass

# USER GET PAYMENT AND TRANSACTION STATUS
class UserStatus(Resource):
  def get(self):
    pass

# USER GET DETAIL TRANSACTION USING TRANSACTION ID AS INPUT
class UserTransactionDetail(Resource):
  def get(self):
    pass

# USER GET INFO ABOUT LATEST TRANSACTION
class UserNewestTransaction(Resource):
  def get(self):
    pass

# USER FILTER TRANSACTIONLIST BY OPERATOR, PRICE, OR TIMESTAMP
class UserFilterTransactions(Resource):
  def get(self):
    pass

# USER GET ALL PRODUCT LIST
class ProductForUser(Resource):
  def get(self):
    pass

# USER GET PRODUCT FILTER Y OPERATOR, PRICE, OR TIMESTAMP
class ProductFilter(Resource):
  def get(self):
    pass

api.add_resource(UserById, '/<int:id>')
api.add_resource(UserProfile, '/<int:id>/profile')
api.add_resource(UserTopUp, '/<int:id>/buying')
api.add_resource(UserStatus, '/<int:id>/status')
api.add_resource(UserTransactionDetail, '/transactions/<int:id>/')
api.add_resource(UserNewestTransaction, '/transactions/<int:id>/newest')
api.add_resource(UserFilterTransactions, '/transactions/filterby/')
api.add_resource(ProductForUser, '/product/list')
api.add_resource(ProductFilter, '/product/filterby/')

