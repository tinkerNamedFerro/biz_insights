import re
import bs4
import requests
import ciso8601

from CoinDict import *
from postgres_db.bizThreads import *

# Load json file for coin list 
# generateCurrenciesList()
with open('data.json') as json_file:
    CD = json.load(json_file)

# Checks message and returns a list of all found tickers
def checkTickerList(message):
    # len(CD)
    found = []
    for row in CD:
        checklist = [(row['name']),(row['name'].lower())]
        # If not flagged in blacklist append
        if row["commonTicker"] == False:
            checklist.append(row['aka'][0].lower())
            checklist.append(row['aka'][0].lower())
        for x in checklist:
            if x in message.split():
                found.append([row['aka'][0],row['coinGeckoId']]) 
           
    return found

def tickerOnlyScrapeArchieve(threadId, tickerDb):
    res = requests.get('https://archive.wakarimasen.moe/biz/thread/'+ threadId)
    soup = bs4.BeautifulSoup(res.content,"html.parser")

    replies = soup.find_all("div", {"class": "text"})
    timeStamps = soup.find_all("time")
    comments = soup.find_all("article", {"class": "post"})
    
    opProcessed = False
    for index in range(0,len(replies)):
        instance = {}
        if not opProcessed:
            # change flag
            opProcessed = True 

            message = replies[index].get_text().replace(">", " ")
            tickerList = checkTickerList(message)
            #  if string is empty this will no execute 
            # print(message)
            for ticker in tickerList:
                #print(ticker)
                #------------------------------------------------------
                # ID
                instance["id"] = int(threadId)
                instance["threadId"] = int(threadId)
                #------------------------------------------------------
                # TIME
                #unix time
                ts = ciso8601.parse_datetime(timeStamps[index]["datetime"])
                # to get time in seconds:
                instance["unixTime"] = int(time.mktime(ts.timetuple()))
                #date String
                instance["dateString"]  = timeStamps[index].get_text()
                #-----------------------------------------------------------
                instance["coinGeckoId"] = ticker[1]
                # Message
                # instance["messageText"] = message
                #print(instance)
                # tickerDb.addTicker(ticker,instance)
                addMention(ticker[0],instance)
        else:
            text = replies[index].get_text().replace(">", " ")
            # print(text)
            tickerList = checkTickerList(text)
            #  if string is empty this will no execute 
            for ticker in tickerList:
                #print(ticker)
                #-----------------------------------------------------------
                # ID (index is always one less)
                instance["id"] = comments[index-1]["id"]
                instance["threadId"] = int(threadId)
                #-----------------------------------------------------------
                # TIME 
                ts = ciso8601.parse_datetime(timeStamps[index]["datetime"])
                # to get time in seconds:
                instance["unixTime"] = int(time.mktime(ts.timetuple()))
                #date String
                instance["dateString"]  = timeStamps[index].get_text()
                #-----------------------------------------------------------
                instance["coinGeckoId"] = ticker[1]
                #print(instance)
                addMention(ticker[0],instance)
                #tickerDb.addTicker(ticker,instance)


            
def getTidsOnPage(page):
    res = requests.get('https://archive.wakarimasen.moe/biz/page/'+ str(page))
    soup = bs4.BeautifulSoup(res.content,"html.parser")
    threads = soup.find_all("article", {"class": "thread"})
    blackList = ["4884770"]
    tids = []
    for thread in threads:
        # Last article doesn't contain thread
        try:
            tid = thread["data-thread-num"]
            if tid not in blackList:
                tids.append(tid)
        except:
            pass
    return tids  
