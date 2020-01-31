from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from ..transactions.models import *
from blueprints import db

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

# ADMIN LOGIN USING SECURITY CODE
class AdminLogin(Resource):
  def post(self):
    pass

# ADMIN GET RANDOM SECURITY CODE
class AdminSecurity(Resource):
  def post(self):
    pass

# ADMIN MANUAL POST TRANSACTION
class AdminPostTransaction(Resource):
  def post(self):
    pass

# ADMIN GET ALL TRANSACTIONS BY USERID
class AdminGetTransactionId(Resource):
  def get(self):
    pass

# ADMIN GET ALL TRANSACTION HISTORY
class AdminGetTransactionList(Resource):
  def get(self):
    pass

# ADMIN FILTER TRANSACTION BY OPERATOR, PRICE, OR, TIMESTAMP
class AdminFilterTransaction(Resource):
  def get(self):
    pass

# ADMIN GET ALL PRODUCT LIST
class AdminProductList(Resource):
  def get(self):
    pass

# ADMIN GET ALL PRODUCT LIST AND FILTER BY OPERATOR, PRICE, AND TIMESTAMP
class AdminFilterProduct(Resource):
  def get(self):
    pass

api.add_resource(AdminLogin, '/login')
api.add_resource(AdminSecurity, '/securitycode')
api.add_resource(AdminPostTransaction, '/transaction')
api.add_resource(AdminGetTransactionId, '/transaction/:id')
api.add_resource(AdminGetTransactionList, '/transaction/list')
api.add_resource(AdminFilterTransaction, '/transaction/filterby/')
api.add_resource(AdminProductList, '/product/list')
api.add_resource(AdminFilterProduct, '/product/filterby/')