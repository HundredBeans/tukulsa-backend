from blueprints import db
from flask_restful import fields
from datetime import datetime

class Users(db.Model):
  __tablename__= "users"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  line_id = db.Column(db.String(255), nullable=False)

  response_fileds = {
    'id' : fields.Integer,
    'lineID' : fields.String
  }

  def __init__(self, line_id):
    self.line_id = line_id