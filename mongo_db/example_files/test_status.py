from pymongo import MongoClient
# pprint library is used to make the output look more pretty
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(os.environ.get('MONGOCONNECTIONSTRING'))
db=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=db.command("serverStatus")
pprint(serverStatusResult)