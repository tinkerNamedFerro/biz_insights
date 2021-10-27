from pymongo import MongoClient
from random import randint
from pprint import pprint

import os
from dotenv import load_dotenv
load_dotenv()

#Step 1: Connect to MongoDB - Note: Change connection string as needed
client = MongoClient(os.environ.get('MONGOCONNECTIONSTRING'), port=27017)
db=client.business

ASingleReview = db.reviews.find_one({})
print('A sample document:')
pprint(ASingleReview)

result = db.reviews.update_one({'_id' : ASingleReview.get('_id') }, {'$inc': {'likes': 1}})
print('Number of documents modified : ' + str(result.modified_count))

UpdatedDocument = db.reviews.find_one({'_id':ASingleReview.get('_id')})
print('The updated document:')
pprint(UpdatedDocument)