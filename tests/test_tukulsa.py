from json import 
import hashlib
import requests
import unittest
from . import app, reset_db,client


class TestUser():
    def test_user_root(self.client):
        data={"line_id":"Ub28f07794c710049e376239fe95e2d2d",
        "display_name": "Ulum"}

        res=client.post("/users", json=data)
        res_data=json.loads(res.data)
        assert res.status_code==200
    
    def test_user_get_its_data(self, client):
        res.client.get("/users", content_type='application/json')
        assert res.status_code==200

    def test_user_topup_pulsa(self,client):
        data={
            "line_id":"Ub28f07794c710049e376239fe95e2d2d",
            "product_code":"htelkomsel1000",
            "phone_number":"081230213222"
        }

        res=client.post('/users/transaction',
        json=data)

        res_json=json.loads(res.data)
        assert res.status_code==200

    def test_get_user_chat(self,client):

        data={"line_id": "Ub28f07794c710049e376239fe95e2d2d"}

        res=client.get("users/chat", json=data, content_type="application/json")
        res_data=json.loads(res.data)
        assert res.status_code==200

    def test_update_user_chat(self, client):
         data={
            "line_id":"Ub28f07794c710049e376239fe95e2d2d",
            "phone_number":"081230213222",
            "nominal":"1000",
            "status_nominal":1,
            "status_number":1,
            "operator":"telkomsel",
            "status_report":2

        }
        res=client.put("users/chat", json=data, content_type="application/json")
        assert res.status_code==200

    def test_user_newest_transaction(self, client):
        data={"line_id":"Ub28f07794c710049e376239fe95e2d2d"}

        res=client.post("/users/transaction/newest", json=data, content_type="application/json")
        assert res.status_code==200

    def test_post_user_filter_transac(self, client):
        data={
            "line_id":"Ub28f07794c710049e376239fe95e2d2d",
            "order_id":"TUKULSAORDER4-1"
        }
        res=client.post("/users/transaction/filterby", json=data)
        assert res.status_code==200

    def test_post_user_order_by_id(self,client):
        data={"order_id": "TUKULSAORDER4-1"}

        res=client.post("/users/transaction/TUKULSAORDER4-1", json=data)
        assert res.status_code==200

    def test_user_edit_transaction_status(self,client):
        data={
            'line_id':"Ub28f07794c710049e376239fe95e2d2d",
            'order_id':"TUKULSAORDER4-1",
            'payment_status':"PENDING",
            "order_status":"PENDING"
        }
        res=client.put("/users/transaction/edit", json=data)
        assert res.status_code==200

    def test_user_get_product_list(self, client):
        res=client.get("/users/product/list", content_type='application/json')
        assert res.status_code==200

    def test_user_post_filter_product(self, client):
        data={"operator": "Telkomsel"}

        res=client.post("/users/product/filterby", json=data)
        assert res.status_code==200

    def test_generate_product_to_db(self, client):
        res=client.get("users/product/generate")
        assert res.status_code==200

    def test_user_post_report(self, client):
        data={'line_id':"Ub28f07794c710049e376239fe95e2d2d",
            'order_id':"TUKULSAORDER4-1"}

        res=client.post("users/report", json=data)
        assert res.status_code==200

    def test_put_report_user(self, client):
        data={
            "line_id":"Ub28f07794c710049e376239fe95e2d2d",
            "text":"Pulsa belum nyampe nih",
            "email":"m.daffa@yahoo.co.id"
        }
        res=client.put("users/report", json=data)
        assert res.status_code==200



