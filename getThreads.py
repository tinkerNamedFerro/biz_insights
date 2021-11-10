import requests
import bs4
import sys, getopt, os 
import re
import pprint
import json
import hashlib
import openpyxl
import datetime
import time
from joblib import Parallel, delayed


from tqdm import tqdm
from selenium import webdriver

from CoinDict import *
from scrapers.ChanOfficial import *
from scrapers.ChanArchieve import *

from mongo_db.tickerTable import *
import multiprocessing as mp


def ThreadIDGet():
    try:
        os.remove('tids.txt')
    except:
        print("Did NOT delete tids.txt")
    url = 'http://boards.4chan.org/biz/catalog'
    driver = webdriver.Chrome()
    driver.get(url)
    res = driver.page_source
    soup = bs4.BeautifulSoup(res, 'lxml')
    body = soup.find('body')
    content = body.find(id="content")
    thread = content.find(id="threads")
    ThR = re.compile(r'(thread-)(\d\d\d\d\d\d\d\d)')

    threadlist = ThR.findall(str(thread))
    ThreadIDs = open("tids.txt", 'a')
    for i in range(1, len(threadlist)):
        ThreadIDs.write(threadlist[i][1] + '\n')
    print('IDs Obtained')
    driver.close()
    ThreadIDs.close()

def TextGet():
    ThreadIDGet()
    try:
        os.remove('text.txt')
    except:
        print("Did NOT delete text.txt")

    tids = open('tids.txt','r')
    tlist = tids.readlines()

    print("Scanning threads")
    tickerDb = MongoDB_Biz_Ticker_Mentions()
    for i in tqdm(range(0, len(tlist)-1)):

        # threadJson = fullThreadScrape(tlist[i][:-2],url)
        tickerOnlyScrape(tlist[i],tickerDb)

    print('Scrape Complete')

def TextGetArchieve(fromPage, toPage):
    # page = 7000

    for page in range(fromPage,toPage):
        try:
            tlist = getTidsOnPage(page)
            # print("Scanning threads")
            tickerDb = MongoDB_Biz_Ticker_Mentions()
            # for i in tqdm(range(0, len(tlist)-1)):
            for i in range(0, len(tlist)-1):
                # threadJson = fullThreadScrape(tlist[i][:-2],url)
                tickerOnlyScrapeArchieve(tlist[i],tickerDb)
        except Exception as e: print("ERROR:" + e)
            
        print("PAGE IS: " + str(page))

def Count(row):
    file = open('text.txt', 'r')
    postlist = file.readlines()
    checklist = [row['aka'][0],row['aka'][0].lower(),(row['name']),(row['name'].lower())]
    Count = 0
    print(checklist)
    for i in range(0,len(postlist)):
        for x in checklist:
            if x in postlist[i].split():
                Count += 1
                break
            else:
                continue
    file.close()
    return Count

# NewBook('tester')
# while True:

    
    # while True:
    #     ThreadIDGet()
    #     TextGet()
    # Update()

def main(argv):

    # Generate list of coins
    generateCurrenciesList()    
    # Load json file for coin list 
    with open('data.json') as json_file:
        CD = json.load(json_file)

    startPage = 0
    endPage = 0
    parallelCount = 0
    try:
        opts, args = getopt.getopt(argv,'s:e:p:')
    except getopt.GetoptError:
        print ('startBrainWallet.py -s <startPage> -e <endPage> -p <parallelCount>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('startBrainWallet.py -s <startPage> -e <endPage> -p <parallelCount>')
            sys.exit()
        elif opt in ("-s", "--start"):
            startPage = int(arg)
        elif opt in ("-e", "--end"):
            endPage = int(arg)
        elif opt in ("-p", "--parallelCount"):
            parallelCount = int(arg)   

    if parallelCount == 0:
        print(startPage)
        TextGetArchieve(startPage,endPage)
    elif parallelCount == -1:
        while True:
            TextGetArchieve(startPage,endPage)
    else:
        # Get work load for each worker
        pageSegmentsDealt = (endPage - startPage)/parallelCount

        # Init pool   
        pool = mp.Pool(parallelCount)

        for instance in range(0,int(parallelCount)):
            instanceStartPage = int(round(startPage+(instance*pageSegmentsDealt)))
            instanceEndPage = int(round(startPage+((instance+1) *pageSegmentsDealt)))
            pool.apply_async(TextGetArchieve, args=(instanceStartPage, instanceEndPage))
            # print(values)

        pool.close()
    

# prevent freeze support error for windows https://minerl.io/docs/notes/windows.html
if __name__ == '__main__':
    main(sys.argv[1:])
