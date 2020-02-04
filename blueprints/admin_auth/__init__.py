from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from flask import Blueprint
from ..admin.models import Admin

bp_auth=Blueprint("admin_auth", __name__)
api=Api(bp_auth, catch_all_404s=True)

class AdminAuth(Resource):
    def get(self):
        parser=reqparse.RequestParser()
        parser.add_argument("line_id", location="args", required=True)
        args=parser.parse_args()
        
        qry=Admin.query.filter_by(line_id= args["line_id"]).first()
        if qry.line_id == args["line_id"]:
            admin_data=marshal(qry, Admin.get_jwt_claims)
            token=create_access_token(identity=args["line_id"], user_claims=admin_data)
            return {'status':token},200
        
        else:
            return {'status': "You Don't Have Authorization"}, 200


api.add_resource(AdminAuth, '')