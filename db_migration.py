from data_parsing import * 
from postgres_db.bizThreads import *
from mongo_db.bizThreads import *


def FullMigration():
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
        print(ticker)
        if ticker != "BTC":
            jsonData = Doc[ticker]
            for row in jsonData:
                time = pd.to_datetime(row['unixTime'],unit='s').strftime("%m/%d/%Y, %H:%M:%S")
                query = "INSERT INTO biztickermentions (mentionId, ticker, threadId, unixTime, datetime) VALUES (%s, '%s', '%s', '%s', '%s') ON CONFLICT (mentionId, ticker) DO UPDATE SET  mentionId=%s;"%(row['id'], ticker, row['threadId'], row['unixTime'], time, row['id'])
                db.update_rows(query)

   




def SingleTickerMigration(ticker, geckoCoinList):
    tickerDb = MongoDB_Biz_Ticker_Mentions()

    if tickerDb.tickerExists(ticker):
        # Get array of mentions
        jsonData = tickerDb.getTicker(ticker)[ticker]
        for row in jsonData:
            time = pd.to_datetime(row['unixTime'],unit='s').strftime("%m/%d/%Y, %H:%M:%S")
            query = "INSERT INTO biztickermentions (mentionId, ticker, threadId, unixTime, datetime) VALUES (%s, '%s', '%s', '%s', '%s') ON CONFLICT (mentionId, ticker) DO UPDATE SET  mentionId=%s;"%(row['id'], ticker, row['threadId'], row['unixTime'], time, row['id'])
            db.update_rows(query)


# geckoCoinList = coinGeckoList()
# SingleTickerMigration("BTC", geckoCoinList)
FullMigration()