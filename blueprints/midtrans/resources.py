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
from mobilepulsa import buying_pulsa

bp_midtrans = Blueprint('midtrans', __name__)
api = Api(bp_midtrans)

username = os.getenv('SERVER_KEY', None)
client_key = os.getenv('CLIENT_KEY', None)
HOST = os.getenv('HOST', None)
STATE = os.getenv('IS_PRODUCTION', None)
if STATE == 'True':
    STATE = True
elif STATE == 'False':
    STATE = False


class MidtransCallback(Resource):
    def option(self):
        return 200

    def post(self):
        # initialize api client object
        api_client = midtransclient.CoreApi(
            is_production=STATE,
            server_key=username,
            client_key=client_key
        )
        req_data = request.get_json()
        mock_notification = {
            "transaction_time": "2020-02-04 22:03:44",
            "gross_amount": "10950.00",
            "currency": "IDR",
            "order_id": "TUKULSA-TUKULSAORDER2-17",
            "payment_type": "gopay",
            "signature_key": "8f83c0dce379431bfdda36f038f5c39383e74ae948207c55b9a29c4ea4e41d74bc393a6628f89d5d4530c5798378625d9850cf6f5ce16107686793eded349c84",
            "status_code": "200",
            "transaction_id": "9bd2c6e3-f1de-4980-b1b5-8ccf9eae2b61",
            "transaction_status": "settlement",
            "fraud_status": "accept",
            "settlement_time": "2020-02-04 22:03:46",
            "status_message": "Success, transaction is found",
            "merchant_id": "G018994973"
        }
        # handle notification JSON sent by Midtrans, it auto verify it by doing get status
        # parameter can be Dictionary or String of JSON
        status_response = api_client.transactions.notification(req_data)

        order_id = status_response['order_id']
        transaction_status = status_response['transaction_status']
        fraud_status = status_response['fraud_status']
        status_code = status_response['status_code']

        print('Transaction notification received. Order ID: {0}. Transaction status: {1}. Fraud status: {2}'.format(
            order_id, transaction_status, fraud_status))
        # Format ORDERID from midtrans to match with transactions table
        formatted_orderID = order_id.replace('TUKULSA-', '')
        # Query table transactions
        selected_trx = Transactions.query.filter_by(order_id= formatted_orderID).first()
        pulsa_code = Product.query.filter_by(id= selected_trx.product_id).first().code
        # Sample transaction_status handling logic
        if status_code == '200':
            # Ubah payment status di transaksi jadi PAID
            selected_trx.payment_status = 'LUNAS'
            selected_trx.order_status = 'PROSES'
            db.session.commit()
            # Nembak mobile pulsa
            buying_pulsa(order_id, selected_trx.phone_number, pulsa_code)
            print('LUNAS')
        elif status_code == '201':
            # Ubah payment status di transaksi jadi PENDING
            selected_trx.payment_status = 'TERTUNDA'
            db.session.commit()
            print('TERTUNDA')
        elif status_code == '202':
            # Ubah payment status di transaksi jadi DENIED
            selected_trx.payment_status = 'DITOLAK'
            db.session.commit()
            print('DITOLAK')
        elif status_code == '407':
            # Ubah payment status di transaksi jadi EXPIRED
            selected_trx.payment_status = 'KADALUWARSA'
            db.session.commit()
            print('KADALUWARSA')
        else:
            print('ERROR')
            
        return 200, {'Content-Type': 'application/json'}


api.add_resource(MidtransCallback, '')
