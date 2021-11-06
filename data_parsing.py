from math import trunc
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import tqdm

from mongo_db.tickerTable import *
from coingecko.util import *
from CoinDict import *


with open('data.json') as json_file:
    CD = json.load(json_file)


def getAllTickerData():
    tickerDb = MongoDB_Biz_Ticker_Mentions()

    Documents, Count = tickerDb.getAll()

    # Get list of all coingecko
    geckoCoinList = coinGeckoList()

    print("Parsing biz coin data:")
    t = tqdm.trange(Count)
    first = True
    for Doc in Documents:
        t.update(1)
        # extract ticker name
        ticker = list(Doc.keys())[1]
        if first:
            first = False
            df = MentionArrayToDf(ticker, Doc[ticker],geckoCoinList)
        else:
            df2 = MentionArrayToDf(ticker, Doc[ticker],geckoCoinList)
            # Check if coin as atleast one day of day 
            if len(df2.index) > 1:
                # Doesn't work like python append thanks pandas
                # https://www.reddit.com/r/learnpython/comments/99u87y/pandas_append_not_working_code_inside/
                df = df.append(df2, ignore_index=True)
    
    return (df)


def getSingleTickerData(ticker, geckoCoinList):
    tickerDb = MongoDB_Biz_Ticker_Mentions()

    if tickerDb.tickerExists(ticker):
        # Get array of mentions
        jsonData = tickerDb.getTicker(ticker)[ticker]
        return MentionArrayToDf(ticker, jsonData,geckoCoinList)

def MentionArrayToDf(ticker, jsonData, geckoCoinList):
    # convert to Dataframe
    df = pd.DataFrame(jsonData)

    # Some posts have timestamps < 0 https://archive.wakarimasen.moe/biz/thread/40386090/
    df = df[df.unixTime > 0]

    # convert unix to datetime
    df['Time'] = pd.to_datetime(df['unixTime'],unit='s')
    # delete meta 
    del df['id']
    del df['threadId']
    del df['unixTime']
    del df['dateString']

    # Not all coins have messageText
    try:
        del df['messageText']
    except:
        pass

    # Sort by day (s.dt.floor('d'))
    # Sort by hour (s.dt.floor('h'))
    # m for minutes and s for seconds
    s = pd.to_datetime(df['Time'])
    df = s.groupby(s.dt.floor('h')).size().reset_index(name='Mentions')
    # Add ticker name 
    df['ticker'] = ticker

    sameTickerCoins = []
    for row in CD:
        if ticker in row["aka"]:
            # print(geckoResponse)
            for coin in geckoCoinList:
                if coin["symbol"] == ticker.lower():
                    sameTickerCoins.append(coin)
                    # geckoResponse = cg.get_price(ids=coin["id"], vs_currencies='usd', include_market_cap='true')
                    # marketCap = (int(geckoResponse[coin["id"]]["usd_market_cap"]))
                    # break
    # Return nothing if coin can't be found in coingecko
    if (len(sameTickerCoins) == 0 ):
        return pd.DataFrame()

    # Whilst scanning ticker in coingecko there are some dicts with the same. Use string similiary on names to get best
    score = 0.0 
    for coinDict in sameTickerCoins:
        similarityCheck = SequenceMatcher(None, coin["name"].lower(), row["name"].lower()).ratio()
        if similarityCheck > score:
            score = similarityCheck
            coin = coinDict
    # print(ticker)
    # print(coin)
    df['coinGeckoId'] = coin["id"]
    df['marketCap'] = coin["market_cap"]

    return (df)


# tickerDf = getSingleTickerData("BTC")
# showSingleLineGraphMarket(tickerDf)
# once = False
# if not once:
#     tickerDf = getAllTickerData()
#     once = True
# showSingleLineGraphMarket(tickerDf)


# print([x['dvpn'] for x in geckoResponse])
