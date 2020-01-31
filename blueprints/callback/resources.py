import requests
import json
from flask import Blueprint
from flask_restful import Api, Resource
from blueprints import db, app
import datetime
import errno
import json
import os
import sys
import tempfile
from argparse import ArgumentParser
# Dari line
import line

bp_callback = Blueprint('callback', __name__)
api = Api(bp_callback)

class LineCallbackResource(Resource):
  def post(self):
    line.callback()

api.add_resource(LineCallbackResource, '/callback')