import json
import requests
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from blueprints import db, app
import json as JSON
import midtransclient
from sqlalchemy import func
from ..transactions.models import Transactions, Product 
from ..users.models import Users

bp_midtrans = Blueprint('midtrans', __name__)
api = Api(bp_midtrans)

username = "SB-Mid-server-45Q3wZH3LKaU6h0BvqRV-Xhu"
client_key="SB-Mid-client-tnH7ODrMQGMO0zvn"
HOST="https://app.sandbox.midtrans.com/snap/v1/transactions" #ganti jadi production LINK (https://app.midtrans.com/snap/v1/transactions)

class MidtransCallback(Resource):
    def option(self):
        return 200

    def post(self):
        
        qry=Transaction.query(func.max(id))
        
        parser=reqparse.RequestParser()
       
        parser.add_argument('phoneNum', location="json")
        parser.add_argument('productName',location="json")
        
        args=parser.parse_args()
        
        qry_product=Product.query.filter_by(code=args['productName'])
        qry_user=Users.query.get(qry.user_id)

        snap = midtransclient.Snap(
            is_production=False, #ganti jadi True untuk production
            server_key=username,
            client_key=client_key)
        
        param = {
        "transaction_details": {
            "order_id": "ORDER-{}".format(qry.id),
            "gross_amount": qry_product.price
        },"item_details":[{
            "id":qry_product.id,
            "price":qry_product.price,
            "quantity":1,
            "name":args['productName'],
            "brand":args['productName'],
            "category":"pulsa",
            "merchant_name":"Tukulsa"
        }],
        "customer_details":{
            "first_name":qry_user.display_name,
            "phone":args['phoneNum'],
        },
        "enabled_payments":["gopay", "akulaku", "bank transfer", "other_va"],
        }


        # transaction redirect url
        transaction = snap.create_transaction(param)
        transaction_url = transaction['redirect_url']
        # print(transaction_url)
        return {"payment_link":transaction_url}, 200


api.add_resource(MidtransCallback, '')
