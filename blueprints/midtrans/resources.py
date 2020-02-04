import json
import requests
from flask import Blueprint, request
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
client_key = "SB-Mid-client-tnH7ODrMQGMO0zvn"
# ganti jadi production LINK (https://app.midtrans.com/snap/v1/transactions)
HOST = "https://app.sandbox.midtrans.com/snap/v1/transactions"


class MidtransCallback(Resource):
    def option(self):
        return 200

    def post(self):
        body = request.get_data(s_text=True)
        print(body)
        return body, 200


api.add_resource(MidtransCallback, '')
