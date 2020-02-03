from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from .models import Users, Chat
from ..transactions.models import *
from blueprints import db, app

bp_users = Blueprint('users', __name__)
api = Api(bp_users)


class UserRootPath(Resource):
    # CREATE USER BY POST
    def post(self):
      # line_id, display_name, user_status
      parser = parser = reqparse.RequestParser()
      parser.add_argument('line_id', location='json', required=True)
      parser.add_argument('display_name', location='json', required=True)
      parser.add_argument('user_status', location='json', required=True)
      args = parser.parse_args()

      # user by line_id
      unique_user = Users.query.filter_by(line_id= args['line_id']).first()
      if unique_user:
        return {'status': 'user already created'}, 200, {'Content-Type': 'application/json'}

      # create new user
      new_user = Users(
          line_id=args['line_id'],
          display_name=args['display_name'],
          user_status=args['user_status'],
      )
      # chat_userid, phone_number, nominal
      db.session.add(new_user)
      db.session.commit()

      # create new chat
      new_chat = Chat(chat_userid=new_user.id)
      db.session.add(new_chat)
      db.session.commit()

      # log
      app.logger.debug('DEBUG : %s', new_user)
      app.logger.debug('DEBUG : %s', new_chat)

      marshal_user = marshal(new_user, Users.response_fileds)
      marshal_chat = marshal(new_chat, Chat.response_fileds)
      return [marshal_user, marshal_chat], 200, {'Content-Type': 'application/json'}

    def delete(self):
      parser = parser = reqparse.RequestParser()
      parser.add_argument('id', location='json', required=True)
      args = parser.parse_args()
      
      target_user = Users.query.filter_by(id=args['id']).first()
      db.session.delete(target_user)
      db.session.commit()

      # log
      app.logger.debug('DEBUG : %s', target_user)

      return {'status': 'user with selected id deleted'}, 200, {'Content-Type': 'application/json'}

    # GET ALL USERS
    def get(self):
      all_user = Users.query.all()
      result = []
      for user in all_user:
        dummy = []
        marshal_user = marshal(user, Users.response_fileds)
        marshal_chat = marshal(user.user_chat, Chat.response_fileds)
        marshal_user['chat'] = marshal_chat
        result.append(marshal_user)

      # log
      app.logger.debug('DEBUG : %s', all_user)
      
      return result, 200, {'Content-Type': 'application/json'}

class UserChat(Resource):      
    # GET BY LINE USER ID
    def get(self):
      parser = parser = reqparse.RequestParser()
      parser.add_argument('line_id', location='json', required=True)
      args = parser.parse_args()
      
      selected_user = Users.query.filter_by(line_id=args['line_id']).first()
      chat_field = selected_user.user_chat[0]

      # log
      app.logger.debug('DEBUG : %s', chat_field)

      marshal_chat = marshal(chat_field, Chat.response_fileds)
      return marshal_chat, 200, {'Content-Type': 'application/json'}

    # PUT METHOD INPUT , STATUS, NOMINAL, NUMBER,
    def put(self):
      parser = parser = reqparse.RequestParser()
      parser.add_argument('line_id', location='json', required=True)
      parser.add_argument('phone_number', location='json')
      parser.add_argument('nominal', location='json')
      parser.add_argument('status_nominal', location='json')
      parser.add_argument('status_number', location='json')
      args = parser.parse_args()

      selected_user = Users.query.filter_by(line_id=args['line_id']).first()
      chat_field = selected_user.user_chat[0]

      if args['phone_number']: chat_field.phone_number = args['phone_number']
      if args['nominal']: chat_field.nominal = int(args['nominal'])
      if args['status_nominal']: chat_field.status_nominal = bool(args['status_nominal'] == 'True')
      if args['status_number']: chat_field.status_number = bool(args['status_number'] == 'True')
      db.session.commit()

      # log
      app.logger.debug('DEBUG : %s', chat_field)

      marshal_chat = marshal(chat_field, Chat.response_fileds)
      return marshal_chat, 200, {'Content-Type': 'application/json'}

class UserById(Resource):
# USER GET SELF TRANSACTION HISTORY
    def get(self):
        pass


class UserProfile(Resource):
    # POST AND GET SELF INFO USER
    def get(self):
        pass

    def post(self):
        pass


class UserTopUp(Resource):
    # USER TOP UP MOBILE BALANCE
    def post(self):
        pass


class UserStatus(Resource):
    # USER GET PAYMENT AND TRANSACTION STATUS
    def get(self):
        pass


class UserTransactionDetail(Resource):
    # USER GET DETAIL TRANSACTION USING TRANSACTION ID AS INPUT
    def get(self):
        pass


class UserNewestTransaction(Resource):
    # USER GET INFO ABOUT LATEST TRANSACTION
    def get(self):
        pass


class UserFilterTransactions(Resource):
    # USER FILTER TRANSACTIONLIST BY OPERATOR, PRICE, OR TIMESTAMP
    def get(self):
        pass


class ProductForUser(Resource):
    # USER GET ALL PRODUCT LIST
    def get(self):
        pass


class ProductFilter(Resource):
    # USER GET PRODUCT FILTER Y OPERATOR, PRICE, OR TIMESTAMP
    def get(self):
        pass



api.add_resource(UserById, '/<int:id>')
api.add_resource(UserProfile, '/<int:id>/profile')
api.add_resource(UserTopUp, '/<int:id>/buying')
api.add_resource(UserStatus, '/<int:id>/status')
api.add_resource(UserTransactionDetail, '/transactions/<int:id>/')
api.add_resource(UserNewestTransaction, '/transactions/<int:id>/newest')
api.add_resource(UserFilterTransactions, '/transactions/filterby/')
api.add_resource(ProductForUser, '/product/list')
api.add_resource(ProductFilter, '/product/filterby/')
api.add_resource(UserRootPath, '')
api.add_resource(UserChat, '/chat')