from kucoin_api.Kucoin import *
import json

def generateCurrenciesList():
    # calling kucoin api to get all coins
    currenciesResponse = getCurrencies()
    coins = []
    # Looping through coins to get ticker and name
    for row in currenciesResponse["data"]:
        ticker = row["currency"]
        name = row["fullName"]

        coin = {"aka":[ticker], 'name':name}
        coins.append(coin)

    # save all coins in json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(coins, f, ensure_ascii=False, indent=4)
    