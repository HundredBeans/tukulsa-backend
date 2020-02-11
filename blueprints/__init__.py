import json
import os
from datetime import datetime, timedelta
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Resource, reqparse
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
CORS(app)

app.config['APP_DEBUG'] = True

### JWT ###
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)

### SQL ALCHEMY CONFIG AWS ###
rds_pass = os.environ.get('RDS_PASS')
rds_link = os.environ.get('RDS_LINK')
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@{}:3306/tukulsaprojecttest'.format(
            rds_pass, rds_link)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@{}:3306/tukulsaproject'.format(
            rds_pass, rds_link)
except Exception as e:
    raise e


# ## SQL ALCHEMY CONFIG LOCAL ###
# mysql_pass = os.environ.get('MYSQL_PASS', '')
# try:
#     env = os.environ.get('FLASK_ENV', 'development')
#     if env == 'testing':
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost:3306/tukulsaprojecttest'.format(
#             mysql_pass)
#     else:
#         app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost:3306/tukulsaproject'.format(
#             mysql_pass)
# except Exception as e:
#     raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#internal super admin

def internal_required(fn):
    @wraps(fn)
    def wrapper (*args,**kwargs):
        verify_jwt_in_request()
        claims=get_jwt_claims()
        try:
            if not claims['role']:
                pass
        except:
            return {'status':'FORBIDDEN', 'message':'Super Administrator Only'}, 403
        else:
            return fn(*args,**kwargs)
    return wrapper

### AFTER REQUEST ###
@app.after_request
def after_request(response):
    try:
        request0 = request.get_json()
    except:
        request0 = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': request0,
            'response': json.loads(response.data.decode('utf-8'))
        }))
    else:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps({
            'status_code': response.status_code,
            'method': request.method,
            'code': response.status,
            'uri': request.full_path,
            'request': request0,
            'response': json.loads(response.data.decode('utf-8'))
        }))
    return response

### IMPORT BLUEPRINTS ###
from blueprints.users.resources import bp_users
app.register_blueprint(bp_users, url_prefix='/users')
from blueprints.admin.resources import bp_admin
app.register_blueprint(bp_admin, url_prefix='/admin')
from blueprints.midtrans.resources import bp_midtrans
app.register_blueprint(bp_midtrans, url_prefix='/notification/handling')

from blueprints.admin_auth.__init__ import bp_auth
app.register_blueprint(bp_auth, url_prefix='/auth')

from blueprints.mobilepulsa.resources import bp_mobPulsa
app.register_blueprint(bp_mobPulsa, url_prefix='/mobilepulsa/callback')



db.create_all()
