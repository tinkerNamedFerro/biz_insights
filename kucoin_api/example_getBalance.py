#Example for get balance of accounts in python
import time
import base64
import hmac
import hashlib
import requests
import json
import pprint

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get('KUCOINKEY')
api_secret = os.environ.get('KUCOINSECRET')
api_passphrase = os.environ.get('KUCOINPASS')
print(api_passphrase)
url = 'https://api.kucoin.com/api/v1/accounts'
now = int(time.time() * 1000)
str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
signature = base64.b64encode(
    hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
passphrase = base64.b64encode(hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
headers = {
    "KC-API-SIGN": signature,
    "KC-API-TIMESTAMP": str(now),
    "KC-API-KEY": api_key,
    "KC-API-PASSPHRASE": passphrase,
    "KC-API-KEY-VERSION": "2"
}
response = requests.request('get', url, headers=headers)
print(response.status_code)
pprint.pprint(response.json())

# #Example for create deposit addresses in python
# url = 'https://openapi-sandbox.kucoin.com/api/v1/deposit-addresses'
# now = int(time.time() * 1000)
# data = {"currency": "BTC"}
# data_json = json.dumps(data)
# str_to_sign = str(now) + 'POST' + '/api/v1/deposit-addresses' + data_json
# signature = base64.b64encode(
#     hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
# passphrase = base64.b64encode(
#     hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
# headers = {
#     "KC-API-SIGN": signature,
#     "KC-API-TIMESTAMP": str(now),
#     "KC-API-KEY": api_key,
#     "KC-API-PASSPHRASE": passphrase,
#     "KC-API-KEY-VERSION": "2",
#     "Content-Type": "application/json" # specifying content type or using json=data in request
# }
# response = requests.request('post', url, headers=headers, data=data_json)
# print(response.status_code)
# print(response.json())