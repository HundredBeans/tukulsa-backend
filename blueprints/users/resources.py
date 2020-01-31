from flask import Blueprint
from flask_restful import Api, Resource, marshal, reqparse
from .models import Users
from blueprints import db

bp_users = Blueprint('users', __name__)
api = Api(bp_users)

class UsersRootResource(Resource):
  def get(self):
    users = Users.query.all()
    return marshal(users, Users.response_fileds), 200

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument('line_id', location='json')
    args = parser.parse_args()
    
    new_user = Users(line_id= args['line_id'])
    db.session.add(new_user)
    db.session.commit()

    return marshal(new_user, Users.response_fileds), 200

api.add_resource(UsersRootResource, '')

