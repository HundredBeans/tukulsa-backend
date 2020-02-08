import hashlib
import json as JSON
# import requests
import re
# from requests.auth import HTTPBasicAuth
import base64
import midtransclient
import os

def midtrans_payment(order_id, label, phone_number, display_name, price ):
    username = os.getenv('SERVER_KEY', None)
    client_key = os.getenv('CLIENT_KEY', None)
    HOST = os.getenv('HOST', None)

    snap = midtransclient.Snap(
        is_production=False,
        server_key=username,
        client_key=client_key)

    param = {
    "transaction_details": {
        "order_id": "TUKULSA-"+order_id,
        "gross_amount":price
    },"item_details":[{
        "id":order_id,
        "price":price,
        "quantity":1,
        "name":label,
        "category":"pulsa",
        "merchant_name":"Tukulsa"
    }],
    "customer_details":{
        "first_name":display_name,
        "phone":phone_number,
    },
    "enabled_payments":["gopay", "akulaku", "bank transfer", "other_va"]
    # "callbacks": {
    #     "finish": "https://demo.midtrans.com"}
    }


    #transaction URL
    # transaction redirect url
    transaction = snap.create_transaction(param)
    transaction_url = transaction['redirect_url']
    # print('transaction_url:')
    return transaction_url