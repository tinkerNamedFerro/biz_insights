from pycoingecko import CoinGeckoAPI
import pickle
import time
from datetime import datetime,timedelta
import pandas as pd 
import numpy as np

def coinGeckoList():
    # Get list of all coingecko
    try:
        data = pickle.load( open( "coingeckoCoins.p", "rb" ) )
    except (OSError, IOError) as e:
        data = None

    if data != None and  time.time() - data[0]  < 3599:
        print("Using pickled coingecko data")
        geckoCoinList = data[1]
    else:
        cg = CoinGeckoAPI()
        geckoCoinList = []
        print("Getting coingecko data", end = '')
        for x in range(1,20):
            response = cg.get_coins_markets(vs_currency='usd', include_market_cap='true', page=x)
            geckoCoinList = geckoCoinList + response
            print(".", end = '')
        print("Done " + str(len(geckoCoinList))  + " collected for pickling")

        data = [time.time(), geckoCoinList]
        pickle.dump( data, open( "coingeckoCoins.p", "wb" ) )

    return geckoCoinList

def getChartById(id):
    cg = CoinGeckoAPI()
    response = cg.get_coin_market_chart_by_id(id=id, vs_currency='usd', days="max")
    df = pd.DataFrame(response["prices"], 
             columns=['unixTime', 
                      'Price'])
    df['unixTime'] = df['unixTime'].astype(str).str[:-3].astype(np.int64)
    df["Time"] = pd.to_datetime(df['unixTime'],unit='s')
    return df

# https://www.coingecko.com/api/documentations/v3#/coins/get_coins__id__market_chart_range
def getHourlyChartById(id):
    cg = CoinGeckoAPI()
    # current time
    dateTimeObj = datetime.now()
    today = time.mktime(dateTimeObj.timetuple())
    # 89 days ago to get hourly data
    eightyNine_days_ago = dateTimeObj - timedelta(days=89)
    past = time.mktime(eightyNine_days_ago.timetuple())
    response = cg.get_coin_market_chart_range_by_id(id=id, vs_currency='usd', from_timestamp=past, to_timestamp=today)
    df = pd.DataFrame(response["prices"], 
             columns=['unixTime', 
                      'Price'])
    df['unixTime'] = df['unixTime'].astype(str).str[:-3].astype(np.int64)
    df["Time"] = pd.to_datetime(df['unixTime'],unit='s')
    return df

