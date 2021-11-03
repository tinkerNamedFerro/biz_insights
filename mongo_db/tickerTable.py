from pymongo import MongoClient
from random import randint

import os
from dotenv import load_dotenv
load_dotenv()


class MongoDB_Biz_Ticker_Mentions:
    def __init__(self):
        # Initialize the connection on the data base.
        #Step 1: Connect to MongoDB - Note: Change connection string as needed
        self.conn = MongoClient(os.environ.get('MONGOCONNECTIONSTRING'), port=27017)
        self.db = self.conn.socials       # Data Base name:  socials
        self.cursor = self.db.bizTickerMentions # Collection name: bizThreads
        
    def create(self, query={}):
        # Insert a new register.
        self.cursor.insert(query)
        
    def read(self, query={}):
        # Read all the register.
        for value in self.cursor.find(query):
            print(value)
        
    def update(self, query_1={}, query_2={}):
        # Change the first item on the list.
        self.cursor.update(query_1, query_2)
    
    def delete(self):
        # Delete all the elements on the list.
        for i in self.cursor.find():
            self.cursor.remove(i)
        
    def threadExists(self, id):
        return True

    def insertThread(self, document):
        if self.threadExists():
            pass
        return

    # updates ticker object with instance 
    def updateTicker(self, ticker,instance):
        # must have ticker in document and instance id must not exist
        where = {
            ticker: {
                "$not": {
                    "$elemMatch": {
                        "id": instance["id"]
                    }
                },
                "$exists" : True
            }
        }
        set = {
            "$push": {
                str(ticker): instance
            }
        }
        self.update(where,set)

    def tickerExists(self,ticker):
        result =  self.cursor.find({ ticker: { "$exists": True } }).count() > 0
        return  result

    def getTicker(self,ticker):
        result =  self.cursor.find({ ticker: { "$exists": True } })
        return  result[0]

    def getAll(self):
        result =  self.cursor.find()
        count =  self.cursor.count_documents({})
        return  result, count

    # check if ticker object exist and either adds or updates with instance 
    def addTicker(self, ticker,instance):
        # Check if ticker exists 
        if self.tickerExists(ticker):
            self.updateTicker(ticker,instance)
        # Create ticker
        else:
            self.cursor.insert_one({ticker:[instance]})


    # def threadIdExists(self,threadId):
        



   