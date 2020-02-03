from blueprints import db
from flask_restful import fields
from datetime import datetime

class Users(db.Model):
  __tablename__= "users"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  line_id = db.Column(db.String(255), nullable=False)
  display_name = db.Column(db.String(255), nullable=False)
  user_status = db.Column(db.String(255), nullable=False)
  user_transactions = db.relationship('transactions', backref='users', lazy='dynamic')

  response_fileds = {
    'id' : fields.Integer,
    'display_name' : fields.String,
    'line_id' : fields.String,
    'user_status' : fields.String
  }

  def __init__(self, line_id, display_name, user_status):
    self.line_id = line_id
    self.display_name = display_name
    self.user_status = user_status