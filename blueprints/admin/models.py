from blueprints import db
from flask_restful import fields
from datetime import datetime

class Admin(db.Model):
    __tablename__="admin"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_id=db.Column(db.String(255), nullable=True)
    name=db.Column(db.String(255), nullable=True)
    security_code=db.Column(db.String(255), nullable=True)
    image=db.Columnn(db.Text, nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at=db.Column(db.Datetime, onupdate=datetime.datetime.now)

    response_fields={
        'id':fields.Integer,
        'line_id':fields.String,
        'name':fields.String,
        'security_code':fields.String,
        'image':fields.String,
        'created_at':fields.DateTime,
        "updated_at":fields.DateTime
    }

    get_jwt_claims={
        'id':fields.Integer,
        'line_id':fields.String,
        'name':fields.String,
        'security_code':fields.String,
        'image':fields.String
    }
    
    def __init__(self,line_id, name, security_code, image ):
        self.line_id=line_id
        self.name=name
        self.security_code=secutity_code
        self.image=image
