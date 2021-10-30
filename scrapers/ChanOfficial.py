import bs4
import requests 

from CoinDict import *

# Load json file for coin list 
# generateCurrenciesList()
with open('data.json') as json_file:
    CD = json.load(json_file)

# Checks message and returns a list of all found tickers
def checkTickerList(message):
    # len(CD)
    found = []
    for row in CD:
        checklist = [row['aka'][0],row['aka'][0].lower(),(row['name']),(row['name'].lower())]
        for x in checklist:
            if x in message.split():
                found.append(row['aka'][0]) 
    return found

def fullThreadScrape(threadId, url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content,"html.parser")
    # print(soup.prettify())
    # return
    replies = soup.find_all("div", {"class": "post reply"})

    thread = {}
    op = soup.find('div', {"class": "post op"})
    #------------------------------------------------------
    # ID
    thread["id"] = int(threadId)
    #------------------------------------------------------
    # TIME
    timeElement = op.find('span', {"class": "dateTime"})
    #unix time
    thread["unixTime"] = int(timeElement['data-utc'])
    #date String
    thread["dateString"]  = timeElement.get_text()
    #-----------------------------------------------------------
    # Message
    thread["messageText"] = op.find('blockquote', {"class": "postMessage"}).get_text()
    # Image

    img = op.find('a', {"class": "fileThumb"})
    if img:
        thread["messageImg"] = img['href']
    thread["comments"] = []
    for i in range(0,len(replies)):
        comment = {}
        #-----------------------------------------------------------
        # ID
        comment["id"] = replies[i].find('a', {"title": "Reply to this post"}).get_text()
        #-----------------------------------------------------------
        # TIME 
        timeElement = replies[i].find('span', {"class": "dateTime"})
        #unix Time
        comment["unixTime"] = int(timeElement['data-utc'])
        #date String
        comment["dateString"]  = timeElement.get_text().split()[0]
        #-----------------------------------------------------------
        # Message
        text = replies[i].blockquote
        # using text to get reference tags
        referencesElements = text.find_all('a', {"class": "quotelink"})
        comment["reference"] = []
        # convert text to string 
        text = text.get_text()
        for ref in referencesElements:
            text = text.replace(ref.get_text(),'')
            comment["reference"].append(ref.get_text()[2:])
        comment["messageText"] = text

        # Image
        img = replies[i].find('a', {"class": "fileThumb"})
        if img:
            comment["messageImg"] = img['href']
        #-----------------------------------------------------------    
        # append comment to list
        thread["comments"].append(comment)

    # Return thread json
    return thread


def tickerOnlyScrape(threadId, tickerDb):
    res = requests.get('http://boards.4chan.org/biz/thread/'+ threadId)
    soup = bs4.BeautifulSoup(res.content,"html.parser")
    # print(soup.prettify())
    # return
    replies = soup.find_all("div", {"class": "post reply"})

    op = soup.find('div', {"class": "post op"})
    message = op.find('blockquote', {"class": "postMessage"}).get_text()
    tickerList = checkTickerList(message)
    #  if string is empty this will no execute 
    for ticker in tickerList:
        instance = {}
        #------------------------------------------------------
        # ID
        instance["id"] = int(threadId)
        instance["threadId"] = int(threadId)
        #------------------------------------------------------
        # TIME
        timeElement = op.find('span', {"class": "dateTime"})
        #unix time
        instance["unixTime"] = int(timeElement['data-utc'])
        #date String
        instance["dateString"]  = timeElement.get_text()
        #-----------------------------------------------------------
        # Message
        # instance["messageText"] = message

        tickerDb.addTicker(ticker,instance)
    for i in range(0,len(replies)):
        comment = {}
        # Message
        text = replies[i].blockquote
        # using text to get reference tags
        referencesElements = text.find_all('a', {"class": "quotelink"})
        # convert text to string 
        text = text.get_text()
        for ref in referencesElements:
            text = text.replace(ref.get_text(),'')
        # comment["messageText"] = text

        tickerList = checkTickerList(text)
        #  if string is empty this will no execute 
        for ticker in tickerList:
            #-----------------------------------------------------------
            # ID
            comment["id"] = replies[i].find('a', {"title": "Reply to this post"}).get_text()
            #-----------------------------------------------------------
            # TIME 
            timeElement = replies[i].find('span', {"class": "dateTime"})
            #unix Time
            comment["unixTime"] = int(timeElement['data-utc'])
            #date String
            comment["dateString"]  = timeElement.get_text().split()[0]
            #-----------------------------------------------------------
            
