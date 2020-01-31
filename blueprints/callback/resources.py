import requests
import json
from flask import Blueprint
from flask_restful import Api, Resource
from blueprints import db, app

bp_callback = Blueprint('callback', __name__)
api = Api(bp_callback)

class LineCallbackResource(Resource):
  def post(self):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

api.add_resource(LineCallbackResource, '/callback')