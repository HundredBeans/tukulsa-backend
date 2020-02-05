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
        # initialize api client object
        api_client = midtransclient.CoreApi(
            is_production=False,
            server_key=username,
            client_key=client_key
        )

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
        status_response = api_client.transactions.notification(
            mock_notification)

        order_id = status_response['order_id']
        transaction_status = status_response['transaction_status']
        fraud_status = status_response['fraud_status']

        print('Transaction notification received. Order ID: {0}. Transaction status: {1}. Fraud status: {2}'.format(
            order_id, transaction_status, fraud_status))

        # Sample transaction_status handling logic

        if transaction_status == 'capture':
            if fraud_status == 'challenge':
                # set transaction status on your databaase to 'challenge'
                print('masuk fraud_status challange')
                # None
            elif fraud_status == 'accept':
                # set transaction status on your databaase to 'success'
                print('masuk fraud_status accept')
                # None
        elif transaction_status == 'cancel' or transaction_status == 'deny' or transaction_status == 'expire':
            print('masuk cancel or deny')
            # set transaction status on your databaase to 'failure'
            # None
        elif transaction_status == 'pending':
            print('masuk pending')
            # set transaction status on your databaase to 'pending' / waiting payment
            # None
        return 200, {'Content-Type': 'application/json'}


api.add_resource(MidtransCallback, '')
