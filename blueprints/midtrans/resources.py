import json
import requests
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from blueprints import db, app

bp_midtrans = Blueprint('midtrans', __name__)
api = Api(bp_midtrans)

class MidtransCallback(Resource):
  def option(self):
    return 200
  def post(self):
    return 200

api.add_resource(MidtransCallback, '')