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



def kucoinGetRequest(route):
    url = 'https://api.kucoin.com' + route
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + route
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
    # print(response.status_code)
    # pprint.pprint(response.json())
    return response.json()


def getSymbols():
    return kucoinGetRequest("/api/v1/symbols")

def getCurrencies():
    return kucoinGetRequest("/api/v1/currencies")

# https://docs.kucoin.com/#get-24hr-stats
def get24HrStats(symbol):
    return kucoinGetRequest("/api/v1/market/stats?symbol=" + symbol + "-USDT")


# print(get24HrStats("btc".upper()))