import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token
from unittest import mock
from unittest.mock import patch

class TestMobPulsa():
    def mock_buy_pulsa(self, client):
        print("Purchasing Success")

    def mock_get_balance(self, client):
        print("Balance Successfully Appear")
        return "100.000"
        
    # @mock.patch.object('requests.post',side_effect=mock_buy_pulsa)
    # @mock.patch.object('requests.get', side_effect=mock_get_balance)
    # def test_buy_pulsa(self, test_buy_pulsa_mock, test_get_balance_mock, client):
