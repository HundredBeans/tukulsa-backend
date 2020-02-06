from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from flask import Blueprint
from ..admin.models import Admin

bp_auth=Blueprint("admin_auth", __name__)
api=Api(bp_auth, catch_all_404s=True)

class AdminAuth(Resource):
    def get(self):
          
        parser=reqparse.RequestParser()
        parser.add_argument("username", location="args")
        parser.add_argument("password", location="args")
        parser.add_argument("security_code", location="args")
        parser.add_argument("line_id",location="args")
        args=parser.parse_args()

        qry=Admin.query.filter_by(line_id= args["line_id"]).first()
        
        #Super Admin Login
        try:
            if args['username']=="admin" and args["password"]=="woka":
                token=create_access_token(identity=args['username'], user_claims={"role":"super_admin"})
                return {"token":token},200
        except:
            return {"status":"You don't have access"},403
        
        #Another Admin
        try:
            if qry.security_code == args["security_code"]:
                admin_data=marshal(qry, Admin.get_jwt_claims)
                token=create_access_token(identity=args["line_id"], user_claims=admin_data)
                return {'status':token},200
        
        except:
            return {'status': "You Don't Have Authorization"}, 200

    def options(self):
        return 200


api.add_resource(AdminAuth, '')