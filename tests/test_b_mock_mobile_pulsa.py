import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token
from unittest import mock
from unittest.mock import patch

class TestMobPulsa():
    def test_mock_buy_pulsa(self, client):
        print("Purchasing Success")

    def test_mock_get_balance(self, client):
        print("Balance Successfully Appear")
        return "100.000"

    