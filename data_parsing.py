from math import trunc
from difflib import SequenceMatcher
import pandas as pd
import numpy as np
import tqdm

from mongo_db.tickerTable import *
from postgres_db.bizThreads import *
from coingecko.util import *
from CoinDict import *


with open('data.json') as json_file:
    CD = json.load(json_file)

def getAllTickerData():
    # Attempt to open graphing data pickle
    try:
        data = pickle.load( open( "graphingDF.p", "rb" ) )
    except (OSError, IOError) as e:
        data = None

    # Check when pickle was last updated 
    if data != None and  time.time() - data[0]  < 3599:
        print("Using pickled dataframe data")
        df = data[1]
    else:
        listOfTickers = getTickers()

        # Get list of all coingecko
        geckoCoinList = coinGeckoList()

        print("Parsing biz coin data:")
        t = tqdm.trange(len(listOfTickers))
        first = True
        for ticker in listOfTickers:
            t.update(1)
            # extract ticker name
            ticker = ticker[0]
            coin_data = getTickerDataPd(ticker)
            if first:
                first = False
                df = MentionArrayToDf(ticker, coin_data,geckoCoinList)
            else:
                df2 = MentionArrayToDf(ticker, coin_data,geckoCoinList)
                # Check if coin as atleast 9 days of activity
                if len(df2.index) > 9:
                    # Doesn't work like python append thanks pandas
                    # https://www.reddit.com/r/learnpython/comments/99u87y/pandas_append_not_working_code_inside/
                    df = df.append(df2, ignore_index=True)

        data = [time.time(), df]
        pickle.dump( data, open( "graphingDF.p", "wb" ) )
    
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
    df = df[df.unixtime > 0]
    geckoId = df['coingeckoid'].iloc[0]
    # convert unix to datetime
    df['Time'] = pd.to_datetime(df['unixtime'],unit='s')
    # delete meta 
    del df['mentionid']
    del df['threadid']
    del df['unixtime']
    del df['datetime']

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
    
    # Get coin data from gecko
    for coin in geckoCoinList:
        if geckoId == coin["id"]:
            break

    df['coinGeckoId'] = coin["id"]
    df['marketCap'] = coin["market_cap"]
    return (df)