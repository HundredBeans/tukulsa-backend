from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from flask import Blueprint
from ..admin.models import Admin
from ..users.models import Report
from datetime import datetime,timedelta
from pytz import timezone

bp_auth=Blueprint("admin_auth", __name__)
api=Api(bp_auth, catch_all_404s=True)

class AdminAuth(Resource):
    def get(self):
          
        parser=reqparse.RequestParser()
        parser.add_argument("username", location="args")
        parser.add_argument("password", location="args")
        parser.add_argument("security_code", location="args")
        args=parser.parse_args()

        #Another Admin
        try:
            if len(args["security_code"]) == 6:
                qry=Admin.query.filter_by(security_code= args["security_code"]).first()
                if qry is not None:
                    date = qry.created_at
                    date_new = date + timedelta(minutes=3)
                    date_now = datetime.now(timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")
                    date_now = datetime.strptime(date_now, "%Y-%m-%d %H:%M:%S")
                    if date >= date_now:
                        admin_data=marshal(qry, Admin.get_jwt_claims)
                        token=create_access_token(identity='admin', user_claims=admin_data)
                        return {'token':token}, 200
                    else:
                        return {'status':"Your security code has been expired, please get the new one!"}
            else:
                report_code = Report.query.filter_by(security_code=args['security_code'])
                if report_code is not None:
                    token = create_access_token(identity='admin')
                    return {'token':token}, 200
        except:
            return {'status': "You Don't Have Authorization"}, 403

    def options(self):
        return 200


api.add_resource(AdminAuth, '')
