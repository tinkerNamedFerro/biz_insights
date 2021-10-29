from CoinDict import *

from mongo_db.tickerTable import *
from graphing.ticker_freq_over_time import *




def getTickerData(ticker):
    tickerDb = MongoDB_Biz_Ticker_Mentions()

    if tickerDb.tickerExists(ticker):
        # Get array of mentions
        jsonData = tickerDb.getTicker(ticker)[ticker]
        # convert to Dataframe
        df = pd.DataFrame(jsonData)
        # convert unix to datetime
        df['Time'] = pd.to_datetime(df['unixTime'],unit='s')
        # delete meta 
        del df['id']
        del df['threadId']
        del df['unixTime']
        del df['dateString']
        del df['messageText']

        # Sort by day (s.dt.floor('d'))
        # Sort by hour (s.dt.floor('h'))
        # m for minutes and s for seconds
        s = pd.to_datetime(df['Time'])
        df = s.groupby(s.dt.floor('d')).size().reset_index(name='Mentions')
        # Add ticker name 
        df['ticker'] = ticker

        return (df)


tickerDf = getTickerData("BTC")
showSingleLineGraph(tickerDf)