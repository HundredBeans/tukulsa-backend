from json import 
import hashlib
import requests
import unittest
from . import app, reset_db,client, create_token

# headers={'Authorization':'Bearer ' + token}

class TestAdmin():
    def test_superadmin(self, client):
        data=dict(
            username="admin",
            password="woka"
        )
        res=client.get("/auth", query_string=data, content_type="application/json")
        assert res.status_code==200
    
    def test_another_admin_6(self, client):
        data=dict(
            security_code="123456"
        )
        res=client.get("/auth", query_string=data, content_type="application/json")
        assert res.status_code==200

    def test_another_admin_less_6(self, client):
        data=dict(
            security_code="12345"
        )
        res=client.get("/auth", query_string=data, content_type="application/json")
        assert res.status_code==200
    

    def test_generate_secure_code(self,client):

        data=dict(line_id= "Ub28f07794c710049e376239fe95e2d2d")
        res=client.post("admin/securitycode", query_string=data)
        assert res.status_code==200

    def test_post_super_admin(self,client):
        # token=create_token()

        data={
            "line_id":"Ub28f07794c710049e376239fe95e2d2d",
            "name":"Ulum",
            "security_code":"123456",
            "image": "apa"}

        res=client.post("admin/super", json=data)
        assert res.status_code==200
    
    def test_put_super_admin(self, client):
        #  token=create_token()

         data={
            "line_id":"Ub28f07794c710049e376239fe95e2d2d",
            "name":"Ulum1",
            "security_code":"123446",
            "image": "yo"}

        res=client.post("admin/super", json=data)
        assert res.status_code==200
    
    def test_admin_post_transaction(self, client):
        # token=create_token()

         data={
            "product_id":2,
            "user_id":1,
            "phone_number":"081230213222 ",
            "order_id": "TUKULSAORDER4-1",
            "operator":"Telkomsel",
            "label":"081230213222 ",
            "nominal":10000,
            "price":11900
            "payment_status":"PENDING",
            "order_status":"SUKSES"
            }
        res=client.post("admin/transaction", json=data)
        assert res.status_code==200

    def test_admin_get_transaction_byid(self, client):
        # token=create_token()
        res=client.get("admin/transaction/1", content_type="application/json")
        assert res.status_code==200

    def test_admin_get_transaction_list(self,client):
        # token=create_token()
        res=client.get("admin/transaction/list", content_type="application/json")
        assert res.status_code==200

    def test_admin_get_transaction_byfilter(self, client):
        # token=create_token()

        data=dict(payment_status="PENDING",
                  order_status="SUKSES")
        
        res=client.get("admin/transaction/filterby", query_string=data)
        assert res.status_code==200

    def test_admin_get_report(self, client):

        # token=create_token()

        data={
            "report_id":1,
            "report_status":"BELUM DISELESAIKAN"
        }

        res=client.get("admin/report", json=data)
        assert res.status_code==200

    def test_admin_update_report(self, client):
        # token=create_token()

        data={
            "report_id":1,
            "report_status":"SELESAI"   
        }

        res=client.put("admin/report", json=data)
        assert res.status_code==200

    def test_admin_get_balance_mobpulsa(self, client):
        # token=create_token()

        res=client.get("admin/balancepulsa", content_type="application/json")
        assert res.status_code==200





    


