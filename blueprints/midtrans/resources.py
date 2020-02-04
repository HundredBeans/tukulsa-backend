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
            'currency': 'IDR',
            'fraud_status': 'accept',
            'gross_amount': '24145.00',
            'order_id': 'test-transaction-321',
            'payment_type': 'bank_transfer',
            'status_code': '201',
            'status_message': 'Success, Bank Transfer transaction is created',
            'transaction_id': '6ee793df-9b1d-4343-8eda-cc9663b4222f',
            'transaction_status': 'pending',
            'transaction_time': '2018-10-24 15:34:33',
            'va_numbers': [{'bank': 'bca', 'va_number': '490526303019299'}]
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
        return 200


api.add_resource(MidtransCallback, '')
