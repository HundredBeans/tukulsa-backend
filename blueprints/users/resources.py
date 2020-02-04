import json
import requests
from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from .models import Users, Chat
from ..transactions.models import *
from blueprints import db, app
from mobilepulsa import get_operator, buying_pulsa
from midtrans import midtrans_payment
from sqlalchemy import desc, asc
from datetime import datetime


bp_users = Blueprint('users', __name__)
api = Api(bp_users)


class UserRootPath(Resource):
    # CREATE USER BY POST
    def post(self):
        # line_id, display_name, user_status
        parser = parser = reqparse.RequestParser()
        parser.add_argument('line_id', location='json', required=True)
        parser.add_argument('display_name', location='json', required=True)
        args = parser.parse_args()

        # user by line_id
        unique_user = Users.query.filter_by(line_id=args['line_id']).first()
        if unique_user:
            return {'status': 'user already created'}, 200, {'Content-Type': 'application/json'}

        # create new user
        new_user = Users(
            line_id=args['line_id'],
            display_name=args['display_name']
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
        parser.add_argument('operator', location='json')
        args = parser.parse_args()

        selected_user = Users.query.filter_by(line_id=args['line_id']).first()
        chat_field = selected_user.user_chat[0]

        if args['phone_number']:
            chat_field.phone_number = args['phone_number']
        if args['nominal']:
            chat_field.nominal = int(args['nominal'])
        if args['status_nominal']:
            chat_field.status_nominal = bool(args['status_nominal'] == 'True')
        if args['status_number']:
            chat_field.status_number = bool(args['status_number'] == 'True')
        if args['operator']:
            chat_field.operator = args['operator']
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
    # USER GET PAYMENT URL
    def post(self):
        parser = parser = reqparse.RequestParser()
        parser.add_argument('line_id', location='json', required=True)
        parser.add_argument('product_code', location='json', required=True)
        parser.add_argument('phone_number', location='json', required=True)
        args = parser.parse_args()
        # butuh selected user
        selected_user = Users.query.filter_by(line_id=args['line_id']).first()
        # butuh selected product
        selected_product = Product.query.filter_by(
            code=args['product_code']).first()
        print(selected_product.id)
        # new transaction
        new_transaction = Transactions(
            user_id=selected_user.id,
            phone_number=args['phone_number'],
            product_id=selected_product.id,
            operator=selected_product.operator,
            label='{} {}'.format(selected_product.operator,
                                 selected_product.nominal),
            nominal=selected_product.nominal,
            price=selected_product.price,
            created_at=datetime.now()
        )
        db.session.add(new_transaction)
        db.session.commit()

        # production = delete --TEST--
        new_transaction.order_id = 'TUKULSAORDER2-{}'.format(
            str(new_transaction.id))
        db.session.commit()

        marshal_trx = marshal(new_transaction, Transactions.response_fields)

        link_payment = midtrans_payment(
            order_id=new_transaction.order_id,
            label=new_transaction.label,
            phone_number=new_transaction.phone_number,
            display_name=selected_user.display_name,
            price=new_transaction.price
        )

        marshal_trx['link_payment'] = link_payment

        # print(marshal_trx)
        return marshal_trx, 200, {'Content-Type': 'application/json'}


class UserStatus(Resource):
    # USER GET PAYMENT AND TRANSACTION STATUS
    def get(self):
        pass


class UserTransactionDetail(Resource):
    # USER GET DETAIL TRANSACTION USING TRANSACTION ID AS INPUT
    def post(self):
        pass


class UserNewestTransaction(Resource):
    # USER GET INFO ABOUT LATEST TRANSACTION
    def post(self):
        parser = parser = reqparse.RequestParser()
        parser.add_argument('line_id', location='json', required=True)
        args = parser.parse_args()

        selected_user = Users.query.filter_by(line_id=args['line_id']).first()

        selected_trx = Transactions.query.filter_by(
            user_id=selected_user.id).order_by(desc(Transactions.id)).first()

        marshal_trx = marshal(selected_trx, Transactions.response_fields)

        return marshal_trx, 200


class UserFilterTransactions(Resource):
    # USER FILTER TRANSACTIONLIST BY OPERATOR, PRICE, OR TIMESTAMP
    def post(self):
        parser = parser = reqparse.RequestParser()
        parser.add_argument('line_id', location='json', required=True)
        parser.add_argument('page', location='args', default=1)
        parser.add_argument('limit', location='args', default=20)
        parser.add_argument("sort", location="args", help="invalid sort value", choices=(
            "desc", "asc"), default="desc")
        parser.add_argument("order_by", location="json", help="invalid order-by value",
                            choices=("id"), default="id")
        args = parser.parse_args()

        # qry = Transactions.query.filter_by(
        #     Transactions.trx_users.line_id.contains(args['line_id'])).all()
        selected_user = Users.query.filter_by(line_id=args['line_id']).first()
        qry = Transactions.query.filter_by(user_id=selected_user.id)
        # print(qry)
        # sort and order
        if args["order_by"] == "id":
            if args["sort"] == "desc":
                qry = qry.order_by(
                    desc(Transactions.id))
            else:
                qry = qry.order_by(Transactions.id)

            # pagination
        offset = (int(args["page"]) - 1)*int(args["limit"])
        qry = qry.limit(int(args['limit'])).offset(offset)

        all_trx = qry.all()
        result = []
        for trx in all_trx:
            marshal_trx = marshal(trx, Transactions.response_fields)
            result.append(marshal_trx)
        return result, 200


class ProductForUser(Resource):
    # USER GET ALL PRODUCT LIST
    def get(self):
        all_product = Product.query.all()
        result = []
        for each in all_product:
            marshal_product = marshal(each, Product.response_fileds)
            result.append(marshal_product)

        return result, 200, {'Content-Type': 'application/json'}


class ProductFilter(Resource):
    # USER GET PRODUCT FILTER Y OPERATOR, PRICE, OR TIMESTAMP
    def post(self):
        parser = parser = reqparse.RequestParser()
        parser.add_argument('page', location='args', default=1)
        parser.add_argument('limit', location='args', default=10)
        parser.add_argument("sort", location="args", help="invalid sort value", choices=(
            "desc", "asc"), default="asc")
        parser.add_argument('operator', location='json', required=True)
        parser.add_argument("order_by", location="json", help="invalid order-by value",
                            choices=("id", "code", "price"), default="code")
        args = parser.parse_args()
        qry = Product.query.filter(
            Product.operator.contains(args['operator']))

        # sort and order
        if args["order_by"] == "id":
            if args["sort"] == "desc":
                qry = qry.order_by(desc(Product.id))
            else:
                qry = qry.order_by(Product.id)
        elif args["order_by"] == "code":
            if args["sort"] == "desc":
                qry = qry.order_by(desc(Product.code))
            else:
                qry = qry.order_by(Product.code)
        elif args["order_by"] == "price":
            if args["sort"] == "desc":
                qry = qry.order_by(desc(Product.price))
            else:
                qry = qry.order_by(Product.price)

        # pagination
        offset = (int(args["page"]) - 1)*int(args["limit"])
        qry = qry.limit(int(args['limit'])).offset(offset)

        selected_products = qry.all()
        # print(selected_products)
        result = []
        for product in selected_products:
            marshal_product = marshal(product, Product.response_fileds)
            result.append(marshal_product)
        print(result)
        return result, 200, {'Content-Type': 'application/json'}


class GenerateProductList(Resource):
    # GET ALL PRODUCT FROM API MOBILE PULSA AND APPEND TO NEW TABLE PROUDCT
    image_path = {
        'telkomsel': 'https://developer.mobilepulsa.net/assets/images/products/telkomsel.png',
        'indosat': 'https://developer.mobilepulsa.net/assets/images/products/indosat.png',
        'xl': 'https://developer.mobilepulsa.net/assets/images/products/xl.png',
        'three': 'https://developer.mobilepulsa.net/assets/images/products/three.png',
        'axis': 'https://developer.mobilepulsa.net/assets/images/products/axis.png',
        'smart': 'https://developer.mobilepulsa.net/assets/images/products/smartfren.png'
    }

    def get(self):
        for index, key in enumerate(self.image_path):
            # get product by operator result in list
            result_product = get_operator('{}'.format(key))['data']
            for each in result_product:
                # condition for add product to product list databsae
                cond_1 = bool(int(each['masaaktif']) > 0)
                cond_2 = bool(each['status'] == "active")
                if cond_1 and cond_2:
                    print(each)
                    new_product = Product(
                        operator=each['pulsa_op'],
                        code=each['pulsa_code'],
                        nominal=each['pulsa_nominal'],
                        price=each['pulsa_price'],
                        valid_to=each['masaaktif'],
                        image=self.image_path['{}'.format(key)]
                    )
                    db.session.add(new_product)
                    db.session.commit()
        return {'status': 'oke'}, 200


api.add_resource(UserById, '/<int:id>')
api.add_resource(UserProfile, '/<int:id>/profile')
api.add_resource(UserTopUp, '/transaction')
api.add_resource(UserStatus, '/<int:id>/status')
api.add_resource(UserTransactionDetail, '/transactions/<int:id>')
api.add_resource(UserNewestTransaction, '/transactions/newest')
api.add_resource(UserFilterTransactions, '/transactions/filterby')
api.add_resource(ProductForUser, '/product/list')
api.add_resource(ProductFilter, '/product/filterby')
api.add_resource(UserRootPath, '')
api.add_resource(UserChat, '/chat')
api.add_resource(GenerateProductList, '/product/generate')
