import pytest, logging, json
from blueprints import app
from app import cache
from flask import request
from . import client, reset_db, create_token
from unittest import mock
from unittest.mock import patch
from mobilepulsa import get_operator, get_order_status, get_balance

class TestMobPulsa():
    def mock_buy_pulsa(self, client):
        print("Purchasing Success")

    def mock_get_balance(self, client):
        print("Balance Successfully Appear")
        return "50.000"

    def mock_get_product(self,client):
        return {
            "data": [
                {
                "pulsa_code": "alfamart100",
                "pulsa_op": "Alfamart Voucher",
                "pulsa_nominal": "Voucher Alfamart Rp 100.000",
                "pulsa_price": 100000,
                "pulsa_type": "voucher",
                "masaaktif": "0",
                "status": "active"
	     	}]}
        
    # @mock.patch.object('requests.post',side_effect=mock_buy_pulsa)
    # @mock.patch.object('requests.get', side_effect=mock_get_balance)
    # def test_buy_pulsa(self, test_buy_pulsa_mock, test_get_balance_mock, client):
    #     token=create_token()
    #     data={}
    
    # @mock.patch.object('requests.post',side_effect=mock_buy_pulsa)
    @mock.patch.object(get_operator, side_effect=mock_get_product)
    def test_get_product(self, test_get_product_mock, test_buy_pulsa_mock, client):
        
        res=client.get("users/product/generate")
        assert res.status_code==200
    
    @mock.patch.object(get_balance, side_effect=mock_get_balance)
    def test_get_nominal_bigger_balance(self, test_get_balance_mock, cient):
        data={ 
            "line_id": "Ub28f07794c710049e376239fe95e2d2d"",
            "product_code":"hindosat300000"
            "phone_number": "085659229599"
        }

        res=client.posy("users/transaction", json=data)
        assert res.status_code==200
