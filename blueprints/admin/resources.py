from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from ..transactions.models import *
from blueprints import db
from .models import Admin
import string
import random

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

# ADMIN LOGIN USING SECURITY CODE
class AdminLogin(Resource):
  @jwt_required
  def post(self):

    parser=reqparse.RequestParser()
    parser.add_argument("security_code", location="json")
    args=parser.parse_args()

    qry=Admin.query.filter_by(security_code=args['security_code']).first()

    if qry.line_id==get_jwt_claims()['line_id']:
      #login success
      return {'status':"Login success"},200
    else:
      return {'status':"Security code is invalid"},403
      

# ADMIN GET RANDOM SECURITY CODE
class AdminSecurity(Resource):
  @jwt_required
  def post(self):
    qry=Admin.query.filter_by(line_id=get_jwt_claims()['line_id']).first()
    size=6
    char=string.digits
    code=(''.join(random.choice(char) for _ in range(0,size)))
    
    qry.security_code=code
    db.session.commit()
    return {"code":code}, 200

# ADMIN MANUAL POST TRANSACTION
class AdminPostTransaction(Resource):
  def post(self):
    parser=reqparse.RequestParser()
    parser.add_argument("product_id", location="json")
    parser.add_argument("user_id", location="json")
    parser.add_argument("phone_number", location="json")
    parser.add_argument("order_id", location="json")
    parser.add_argument("operator", location="json")
    parser.add_argument("label", location="json")
    parser.add_argument("nominal", location="json")
    parser.add_argument("price", location="json")
    parser.add_argument("payment_status", location="json")
    parser.add_argument("order_status", location="json")
    parser.add_argument("created_at", location="json")
    args=parser.parse_args()
    
    qry=Transactions.query.filter_by(order_id=args['order_id'])
    if qry is None:
      transaction=Transactions(args['user_id'], args['phone_number'],args['product_id'],
      args['operator'], args['label'], args['nominal'], args['price'],args['created_at'])

      db.session.add(transaction)
      db.session.commit()

      return marshal(transaction, Transactions.response_fields), 200
    else:
      return {'status':"transaction detail is already existed"},403

# ADMIN GET ALL TRANSACTIONS BY USERID
class AdminGetTransactionId(Resource):
  def get(self,id):
    qry=Transactions.query.filter_by(id=id).first()

    if qry is None:
      return{'status':'NOT FOUND'}, 404
    else:
      return marshal(qry, Transactions.response_fields),200

# ADMIN GET ALL TRANSACTION HISTORY
class AdminGetTransactionList(Resource):
  def get(self):
    parser=reqparse.RequestParser()
    parser.add_argument('p', location='args', type=int,default=1)  
    parser.add_argument('rp', location='args', type=int, default=20)
    args=parser.parse_args()

    qry=Transactions.query

    offset=(args['p']*args['rp'])-args['rp']

    #looping all quaery to provide list of products
    rows=[]
    for row in qry.limit(args['rp']).offset(offset).all():
        rows.append(marshal(row, Transactions.response_fields))
    return rows, 200


# ADMIN FILTER TRANSACTION BY OPERATOR, PRICE, OR, TIMESTAMP
class AdminFilterTransaction(Resource):
  def get(self):
    parser = parser = reqparse.RequestParser()
    parser.add_argument('page', location='args', default=1)
    parser.add_argument('limit', location='args', default=10)
    parser.add_argument("sort", location="args", help="invalid sort value", choices=(
        "desc", "asc"), default="asc")
    parser.add_argument('operator', location='json', required=True)
    parser.add_argument("order_by", location="json", help="invalid order-by value",
                        choices=("id", "code", "price"), default="code")
    args = parser.parse_args()
    qry = Transactions.query.filter(
        Product.operator.contains(args['operator']))

    # sort and order
    if args["order_by"] == "id":
        if args["sort"] == "desc":
            qry = qry.order_by(desc(Transactions.id))
        else:
            qry = qry.order_by(Transactions.id)
    elif args["order_by"] == "code":
        if args["sort"] == "desc":
            qry = qry.order_by(desc(Transactions.label))
        else:
            qry = qry.order_by(Transactions.label)
    elif args["order_by"] == "price":
        if args["sort"] == "desc":
            qry = qry.order_by(desc(Transactions.price))
        else:
            qry = qry.order_by(Transactions.price)

    # pagination
    offset = (int(args["page"]) - 1)*int(args["limit"])
    qry = qry.limit(int(args['limit'])).offset(offset)

    selected_products = qry.all()
    # print(selected_products)
    result = []
    for product in selected_products:
        marshal_product = marshal(product, Product.response_fileds)
        result.append(marshal_product)
    print(result)
    return result, 200, {'Content-Type': 'application/json'}
  

# ADMIN GET ALL PRODUCT LIST
class AdminProductList(Resource):
  def get(self):
    parser=reqparse.RequestParser()
    parser.add_argument('p', location='args', type=int,default=1)  
    parser.add_argument('rp', location='args', type=int, default=20)
    args=parser.parse_args()

    qry=Product.query

    offset=(args['p']*args['rp'])-args['rp']

    #looping all quaery to provide list of products
    rows=[]
    for row in qry.limit(args['rp']).offset(offset).all():
        rows.append(marshal(row, Product.response_fields))
    return rows, 200

# ADMIN GET ALL PRODUCT LIST AND FILTER BY OPERATOR, PRICE, AND TIMESTAMP
class AdminFilterProduct(Resource):
  def get(self):
      parser = parser = reqparse.RequestParser()
      parser.add_argument('page', location='args', default=1)
      parser.add_argument('limit', location='args', default=10)
      parser.add_argument("sort", location="args", help="invalid sort value", choices=(
          "desc", "asc"), default="asc")
      parser.add_argument('operator', location='json', required=True)
      parser.add_argument("order_by", location="json", help="invalid order-by value",
                          choices=("id", "code", "price"), default="code")
      args = parser.parse_args()
      qry = Product.query.filter(
          Product.operator.contains(args['operator']))

      # sort and order
      if args["order_by"] == "id":
          if args["sort"] == "desc":
              qry = qry.order_by(desc(Product.id))
          else:
              qry = qry.order_by(Product.id)
      elif args["order_by"] == "code":
          if args["sort"] == "desc":
              qry = qry.order_by(desc(Product.code))
          else:
              qry = qry.order_by(Product.code)
      elif args["order_by"] == "price":
          if args["sort"] == "desc":
              qry = qry.order_by(desc(Product.price))
          else:
              qry = qry.order_by(Product.price)

      # pagination
      offset = (int(args["page"]) - 1)*int(args["limit"])
      qry = qry.limit(int(args['limit'])).offset(offset)

      selected_products = qry.all()
      # print(selected_products)
      result = []
      for product in selected_products:
          marshal_product = marshal(product, Product.response_fileds)
          result.append(marshal_product)
      print(result)
      return result, 200, {'Content-Type': 'application/json'}

api.add_resource(AdminLogin, '/login')
api.add_resource(AdminSecurity, '/securitycode')
api.add_resource(AdminPostTransaction, '/transaction')
api.add_resource(AdminGetTransactionId, '/transaction/:id')
api.add_resource(AdminGetTransactionList, '/transaction/list')
api.add_resource(AdminFilterTransaction, '/transaction/filterby/')
api.add_resource(AdminProductList, '/product/list')
api.add_resource(AdminFilterProduct, '/product/filterby/')



