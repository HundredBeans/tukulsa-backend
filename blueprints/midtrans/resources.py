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
import base64
from midtrans import midtrans_payment

bp_midtrans = Blueprint('midtrans', __name__)
api = Api(bp_midtrans)

username = "SB-Mid-server-45Q3wZH3LKaU6h0BvqRV-Xhu"
client_key="SB-Mid-client-tnH7ODrMQGMO0zvn"
HOST="https://app.sandbox.midtrans.com/snap/v1/transactions" #ganti jadi production LINK (https://app.midtrans.com/snap/v1/transactions)

class MidtransCallback(Resource):
    def option(self):
        return 200
    

    def post(self):

        data=midtrans_payment("100", "indosat25000", "085659229599", "woka", 26000)
        return {"payment":data},200


api.add_resource(MidtransCallback, '')
