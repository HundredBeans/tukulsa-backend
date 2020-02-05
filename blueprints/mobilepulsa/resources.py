import hashlib
import json as JSON
import requests
from flask import Blueprint, request
from flask_restful import Api, Resource, marshal, reqparse
from blueprints import db, app
from sqlalchemy import func
from ..transactions.models import Transactions, Product 
from ..users.models import Users

bp_mobPulsa = Blueprint('mobPulsa', __name__)
api = Api(bp_mobPulsa)

username = "085659229599"
password = "9415e33f6d2098d7"

class MobilePulsaCallback(Resource):
    '''
    Class for Handling Callback from Mobile Pulsa API
    
    Methods
    ------
        post(self)
            to get callback from Mobile Pulsa API and perform update on transaction table

        options(self)
            to prevent CORS when performing callback
    '''
    def options(self):
        return 200
    
    def post(self):
        # Get Callback JSON
        req_data = request.get_json()
        order_id = req_data['request']['data']['ref_id']
        # Query fro specific Transactions obtained from callback
        selected_trx = Transactions.query.filter_by(order_id= order_id).first()
        # Update order status based on callback status
        if req_data['request']["data"]["status"] == 1:
            selected_trx.order_status = "SUCCESS"
            db.session.commit()
        elif req_data['request']["data"]["status"] == 0:
            selected_trx.order_status = "PROCESS"
            db.session.commit()
        elif req_data['request']["data"]["status"] == 2:
            selected_trx.order_status = "FAILED"
            db.session.commit()

        return req_data, 200, {'Content-Type': 'application/json'}

api.add_resource(MobilePulsaCallback, '')