import hashlib
import json as JSON
import requests
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from blueprints import db, app
from sqlalchemy import func
from ..transactions.models import Transactions, Product 
from ..users.models import Users

bp_mobPulsa = Blueprint('mobPulsa', __name__)
api = Api(bp_mobPulsa)

username = "085659229599"
password = "9415e33f6d2098d7"

class ProductList(Resource):
    def get(self):

        parser=reqparse.RequestParser()
       
        parser.add_argument('operator', location="args")
       
        args=parser.parse_args()
        operator = args["operator"]

        gabung = username+password+"pl"
        signature = hashlib.md5(gabung.encode()).hexdigest()
        
        json = """{
            \"commands\" : \"pricelist\",
            \"username\" : \"""" + username + """\",
            \"sign\"     : \"""" + signature + """\"
        }"""

        url = "https://testprepaid.mobilepulsa.net/v1/legacy/index/pulsa/"+operator

        headers = {'content-type': 'application/json'}

        data = requests.post(url, data=json, headers=headers, timeout=30).text
        parsed = JSON.loads(data)
        # return parsed
        return JSON.dumps(parsed, indent=4), 200

class BuyPulsa(Resource):
    def post(self):
        qry=Transaction.query(func.max(id))

        # parser=reqparse.RequestParser()
        # parser.add_argument('id', location="json")
        # parser.add_argument('phoneNum', location="json")
        # args=parser.parse_args()

        
        orderID= "ORDER-{}".format(qry.id)
        numberPhone=qry.phone_number
        pulsa_code=qry.label

        gabung = username+password+orderID
        signature = hashlib.md5(gabung.encode()).hexdigest()
        url = "https://testprepaid.mobilepulsa.net/v1/legacy/index"
        headers = {'content-type': 'application/json'}

        json = """{
            \"commands\":\"topup\",
            \"username\":\"""" + username + """\",
            \"ref_id\":\""""+orderID+"""\",
            \"hp\":\"""" + numberPhone + """\",
            \"pulsa_code\":\"""" + pulsa_code+"""\",
            \"sign\"     : \"""" + signature + """\"
        }"""
        data_buying = requests.post(
            url, data=json, headers=headers, timeout=30).text
        parsed = JSON.loads(data_buying)

        return JSON.dumps(parsed, indent=4), 200

class GetStatus(Resource):
    def get(self):
        qry=Transaction.query(func.max(id))

        orderID= "ORDER-{}".format(qry.id)
        url = "https://testprepaid.mobilepulsa.net/v1/legacy/index"
        headers = {'content-type': 'application/json'}

        json = """{
            \"commands\":\"inquiry\",
            \"username\":\"""" + username + """\",
            \"ref_id\":\"""" + orderID + """\",
            \"sign\"     : \"""" + signature + """\"
        }"""
        data = requests.post(url, data=json, headers=headers, timeout=30).text
        parsed = JSON.loads(data)

        return JSON.dumps(parsed, indent=4),200

api.add_resource(ProductList, '')
api.add_resource(BuyPulsa, '')
api.add_resource(GetStatus, '')