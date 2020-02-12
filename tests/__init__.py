import pytest, json,logging
from app import app
from flask import Flask,request
from app import cache
from blueprints import app, db
from blueprints.users.models import *
import hashlib

def reset_db():
    db.drop_all()
    db.create_all()
    
    # Client=Users("Ub28f07794c710049e376239fe95e2d2d", "Ulum")
    # db.session.add(Client)
    # db.session.commit()

@pytest.fixture
def client(request):
    return app.test_client(request)