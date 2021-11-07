import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

from .db import Database
from .log import LOGGER

# Create database class
db = Database(
    os.environ.get('PSQL_HOST'),
    os.environ.get('PSQL_USERNAME'),
    os.environ.get('PSQL_PASSWORD'),
    os.environ.get('PSQL_PORT'),
    os.environ.get('PSQL_NAME')
)


def init_script():
    """Execute queries against PostgreSQL database."""
    standard_results = db.select_rows("select * from biztickermentions")
    # dict_cursor_results = db.select_rows_dict_cursor(queries[0])
    display_query_results(standard_results, cursor_type='standard')
    # display_query_results(dict_cursor_results, cursor_type='dictcursor')


def display_query_results(rows, cursor_type=None):
    """Log results of query to console."""
    LOGGER.info(f'Results from {cursor_type}:')
    for row in rows:
        LOGGER.info(row)

def addMention(ticker, row):
    # Convert to date time
    time = pd.to_datetime(row['unixTime'],unit='s').strftime("%m/%d/%Y, %H:%M:%S")

    query = """INSERT INTO biztickermentions (mentionId, ticker, coinGeckoId, threadId, unixTime, datetime) 
    VALUES (%s, '%s', '%s', '%s', '%s', '%s') 
    ON CONFLICT (mentionId, ticker) DO UPDATE SET  mentionId=%s;
    """%(row['id'], ticker, row['coinGeckoId'], row['threadId'], row['unixTime'], time, row['id'])

    db.update_rows(query)

def getTickers():
    query = """SELECT DISTINCT ticker FROM biztickermentions;"""
    test = db.select_rows(query)
    return test

def getTickerDataPd(ticker):
    query = """SELECT mentionId, ticker, coinGeckoId, threadId, unixTime, datetime FROM biztickermentions WHERE ticker='%s';"""%(ticker)
    pd = db.queryToPD(query)
    return pd