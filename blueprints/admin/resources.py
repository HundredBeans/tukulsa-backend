from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from ..transactions.models import *
from mobilepulsa import get_balance
from blueprints import db, internal_required
from sqlalchemy import func, distinct
from sqlalchemy import desc, asc
from .models import Admin
from ..users.models import Report
import string
import random
import calendar
import datetime

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

# ADMIN LOGIN USING SECURITY CODE

class SuperAdmin(Resource):
  # @internal_required
  def post(self):
    parser=reqparse.RequestParser()
    parser.add_argument("line_id", location="json")
    parser.add_argument("name", location="json")
    parser.add_argument("security_code", location="json")
    parser.add_argument("image", location="json")
    args=parser.parse_args()

    admin_add=Admin(args['line_id'], args['name'], args['security_code'], args['image'])
    db.session.add(admin_add)
    db.session.commit()

    return marshal(admin_add, Admin.response_fields), 200
  # @jwt_required
  def put(self):
    parser=reqparse.RequestParser()
    parser.add_argument("id", location="json")
    parser.add_argument("line_id", location="json")
    parser.add_argument("name", location="json")
    parser.add_argument("security_code", location="json")
    parser.add_argument("image", location="json")
    args=parser.parse_args()
 
    qry=Admin.query.get(args['id'])

    if args["line_id"]:
      qry.line_id=args["line_id"]
    else:
      qry.line_id=qry.line_id

    if args["name"]:
      qry.name=args["name"]
    else:
      qry.name=qry.name
    
    if args["security_code"]:
      qry.security_code=args["security_code"]
    else:
      qry.security_code=qry.security_code
    
    if args["image"]:
      qry.image=args["image"]
    else:
      qry.image=qry.image

    db.session.commit()

    return {'status':"Data Successfully Updated"}, 200
  
  def options(self):
        return 200

# class AdminLogin(Resource):
#   # @jwt_required
#   def post(self):

#     parser=reqparse.RequestParser()
#     parser.add_argument("security_code", location="json")
#     args=parser.parse_args()

#     qry=Admin.query.filter_by(security_code=args['security_code']).first()

#     if qry.line_id==get_jwt_claims()['line_id']:
#       #login success
#       return {'status':"Login success"},200
#     else:
#       return {'status':"Security code is invalid"},403
      

# ADMIN GET RANDOM SECURITY CODE
class AdminSecurity(Resource):

  def post(self):
    parser=reqparse.RequestParser()
    parser.add_argument("line_id", location="args")
    args=parser.parse_args()

    qry=Admin.query.filter_by(line_id=args['line_id']).first()

    if qry is None:
       return {"status":"You Cannot Access This Page"}, 200

    size=6
    char=string.digits
    code=(''.join(random.choice(char) for _ in range(0,size)))
    
    qry.security_code=code
    db.session.commit()
    return {"code":code}, 200
  
  def options(self):
        return 200

# ADMIN MANUAL POST TRANSACTION
class AdminPostTransaction(Resource):
  # @jwt_required
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

  def options(self):
      return 200

# ADMIN GET ALL TRANSACTIONS BY USERID
class AdminGetTransactionId(Resource):
  # @jwt_required
  def get(self,id):
    qry=Transactions.query.filter_by(id=id).first()

    if qry is None:
      return{'status':'NOT FOUND'}, 404
    else:
      return marshal(qry, Transactions.response_fields),200
  
  def options(self,id):
        return 200

# ADMIN GET ALL TRANSACTION HISTORY
class AdminGetTransactionList(Resource):
  # @jwt_required
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

  def options(self):
        return 200


# ADMIN FILTER TRANSACTION BY OPERATOR, PRICE, OR, TIMESTAMP
class AdminFilterTransaction(Resource):
  # @jwt_required
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument('page', location='args', default=1)
    parser.add_argument('limit', location='args', default=10)
    parser.add_argument("sort", location="args", help="invalid sort value", choices=("desc", "asc"), default="desc")
    parser.add_argument('operator', location='args')
    parser.add_argument('days_ago', location='args', type=int, default=30)
    parser.add_argument('payment_status', location='args', help="invalid payment-status value", choices=("LUNAS", "TERTOLAK", "DITUNDA", "KADALUARSA"))
    parser.add_argument('order_status', location='args', help="invalid order-status value", choices=("BELUM DIPROSES", "PROSES", "SUKSES", "GAGAL"))
    parser.add_argument("order_by", location="args", help="invalid order-by value",choices=("id", "label", "price", "created_at"), default="label")
    args = parser.parse_args()
    
    
    qry = Transactions.query
    # qry_coba=qry.filter(Transactions.created_at.like('%2018%'))
    if args['days_ago']:
      current_time = datetime.datetime.now(timezone('Asia/Jakarta'))
      days_ago = current_time - datetime.timedelta(days=args['days_ago'])
      qry = qry.filter(Transactions.created_at > days_ago).all()
    if args['operator']:
      qry = qry.filter_by(operator=args['operator'])
    if args['payment_status']:
      qry = qry.filter_by(payment_status=args['payment_status'])
    if args['order_status']:
      qry = qry.filter_by(order_status=args['order_status'])

    if args["order_by"] == "id":
        if args["sort"] == "desc":
            qry = qry.order_by(Transactions.id.desc())
        else:
            qry = qry.order_by(Transactions.id)
    elif args["order_by"] == "label":
        if args["sort"] == "desc":
            qry = qry.order_by(Transactions.label.desc())
        else:
            qry = qry.order_by(Transactions.label)
    elif args["order_by"] == "price":
        if args["sort"] == "desc":
            qry = qry.order_by(Transactions.price.desc())
        else:
            qry = qry.order_by(Transactions.price)



    # pagination
    offset = (int(args["page"]) - 1)*int(args["limit"])
    qry = qry.limit(int(args['limit'])).offset(offset)

    selected_transactions = qry.all()
    # print(selected_products)
    qry_paid_transaction=Transactions.query.filter_by(order_status="DIPROSES").all()
    result = []
    summary={}
    for transaction in selected_transactions:
        marshal_transaction = marshal(transaction, Transactions.response_fields)
        result.append(marshal_transaction)
    summary['transaction']=result
    summary["total_transaction"]=sum(qry_paid_transaction.price)
    summary["total_profit"]=200*len(qry_paid_transaction)
    print(result)
    return summary, 200, {'Content-Type': 'application/json'}

  def options(self):
        return 200
  

# ADMIN GET ALL PRODUCT LIST
class AdminProductList(Resource):
  # @jwt_required
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
  
  def options(self):
        return 200

# ADMIN GET ALL PRODUCT LIST AND FILTER BY OPERATOR, PRICE, AND TIMESTAMP
class AdminFilterProduct(Resource):
  # @jwt_required
  def get(self):
      parser = reqparse.RequestParser()
      parser.add_argument('page', location='args', default=1)
      parser.add_argument('limit', location='args', default=10)
      parser.add_argument("sort", location="args", help="invalid sort value", choices=(
          "desc", "asc"), default="asc")
      parser.add_argument('operator', location='args', required=True)
      parser.add_argument("order_by", location="args", help="invalid order-by value",
                          choices=("id", "code", "price"), default="id")
      args = parser.parse_args()
      qry = Product.query.filter_by(operator=args['operator'])

      # sort and order
      if args["order_by"] == "id":
          if args["sort"] == "desc":
              qry = qry.order_by(Product.id.desc())
          else:
              qry = qry.order_by(Product.id)
      elif args["order_by"] == "code":
          if args["sort"] == "desc":
              qry = qry.order_by(Product.code.desc())
          else:
              qry = qry.order_by(Product.code)
      elif args["order_by"] == "price":
          if args["sort"] == "desc":
              qry = qry.order_by(Product.price.desc())
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

  def options(self):
        return 200

class AdminReport(Resource):
    """
    Page for Admin to update and get report from users

    Methods
    --
        get(self) : Get all report
        put(self) : Update report status or Get specific report by report id
    """
    def get(self):
        parser = parser = reqparse.RequestParser()
        parser.add_argument('report_status', location='args')
        args = parser.parse_args()

        qry = Report.query
        if args['report_status']:
          qry = qry.filter_by(status=args['report_status'])
        report_all = qry.order_by(desc(Report.id)).all()
        report_list = []
        for report in report_all:
            marshal_report = marshal(report, Report.response_fields)
            report_list.append(marshal_report)
        
        return report_list, 200, {'Content-Type': 'application/json'}

    def put(self):
        parser = parser = reqparse.RequestParser()
        parser.add_argument('report_id', location='json', required=True)
        parser.add_argument('report_status', location='json')
        args = parser.parse_args()

        report_qry = Report.query.get(args['report_id'])

        if args['report_status']:
            report_qry.status = args['report_status']

        return marshal(report_qry, Report.response_fields), 200, {'Content-Type': 'application/json'}

    def options(self):
        return 200

class GetBalance(Resource):
    def get(self):      
        return {'balance': get_balance}, 200

api.add_resource(SuperAdmin, '/super')
# api.add_resource(AdminLogin, '/login')
api.add_resource(AdminSecurity, '/securitycode')
api.add_resource(AdminPostTransaction, '/transaction')
api.add_resource(AdminGetTransactionId, '/transaction/<int:id>')
api.add_resource(AdminGetTransactionList, '/transaction/list')
api.add_resource(AdminFilterTransaction, '/transaction/filterby')
api.add_resource(AdminProductList, '/product/list')
api.add_resource(AdminFilterProduct, '/product/filterby')
api.add_resource(AdminReport, '/report')
api.add_resource(GetBalance,"/balancepulsa")


