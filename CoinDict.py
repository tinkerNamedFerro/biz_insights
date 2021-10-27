from kucoin_api.Kucoin import *
import json

blackList = ["KEEP", "FLOW", "MASK", "SUPER","SCLP", "GO", "MATTER","MASK", "NFT", "TIME", "JST", "MAN", "FEAR", "LAYER", "WIN", "GOD", "BUY","PUSH", "FORM", "FRONT", "SNT", "CARD", "STND", "ASK"]

def generateCurrenciesList():
    # calling kucoin api to get all coins
    currenciesResponse = getCurrencies()
    coins = []
    # Looping through coins to get ticker and name
    for row in currenciesResponse["data"]:
        ticker = row["currency"]
        name = row["fullName"]

        coin = {"aka":[ticker], 'name':name}
        # Don't add ticker if in blacklist
        if ticker not in blackList:
            coins.append(coin)

    # save all coins in json
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(coins, f, ensure_ascii=False, indent=4)
    