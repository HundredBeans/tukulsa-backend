from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from ..transactions.models import *
from blueprints import db
from models import Admin
import stringimport random

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

# ADMIN LOGIN USING SECURITY CODE
class AdminLogin(Resource):
  def post(self):

    pass

# ADMIN GET RANDOM SECURITY CODE
class AdminSecurity(Resource):
  @jwt_required
  def post(self):
    qry=Admin.query.filter_by(line_id=get_jwt_claims()['line_id']).first()
    size=6
    char=string.digits:
    code=(''.join(random.choice(char) for _ in range(0,size)))
    
    qry.security_code=code
    db.session.commit()
    return {"code":code}, 200

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