

import hashlib
import json as JSON
import requests
import os

username = os.getenv('MOBILEPULSA_USERNAME', None)
password = os.getenv('MOBILEPULSA_PASSWORD', None)
base_url = 'https://api.mobilepulsa.net/v1/legacy/index'


def get_operator(operator):
    gabung = username+password+"pl"
    signature = hashlib.md5(gabung.encode()).hexdigest()

    json = """{
        \"commands\" : \"pricelist\",
        \"username\" : \"""" + username + """\",
        \"sign\"     : \"""" + signature + """\"
    }"""

    url = "{}/pulsa/{}".format(base_url, operator)

    headers = {'content-type': 'application/json'}

    data = requests.post(url, data=json, headers=headers, timeout=30).text
    parsed = JSON.loads(data)
    return parsed
    # return JSON.dumps(parsed, indent=4)


def buying_pulsa(orderID, numberPhone, pulsa_code):
    gabung = username+password+orderID
    signature = hashlib.md5(gabung.encode()).hexdigest()
    url = base_url
    headers = {'content-type': 'application/json'}

    json = """{
        \"commands\":\"topup\",
        \"username\":\"""" + username + """\",
        \"ref_id\":\""""+orderID+"""\",
        \"hp\":\"""" + numberPhone + """\",
        \"pulsa_code\":\"""" + pulsa_code+"""\",
        \"sign\"     : \"""" + signature + """\"
    }"""
    data_buying = requests.post(
        url, data=json, headers=headers, timeout=30).text
    parsed = JSON.loads(data_buying)
    return parsed
    # print(JSON.dumps(parsed, indent=4))


def get_order_status(orderID):
    gabung = username+password+orderID
    signature = hashlib.md5(gabung.encode()).hexdigest()
    url = base_url
    headers = {'content-type': 'application/json'}

    json = """{
        \"commands\":\"inquiry\",
        \"username\":\"""" + username + """\",
        \"ref_id\":\"""" + orderID + """\",
        \"sign\"     : \"""" + signature + """\"
    }"""
    data = requests.post(url, data=json, headers=headers, timeout=30).text
    parsed = JSON.loads(data)

    print(JSON.dumps(parsed, indent=4))
