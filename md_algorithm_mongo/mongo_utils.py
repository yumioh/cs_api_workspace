import os
from pymongo import MongoClient
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

#mongoDB to DataFrame
class MongoDBHandler:

    def __init__(self, db_name, collection_name) :
        #mongoDB 연결
        mongo_uri = os.getenv('MONGO_DB')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
    
    def fetch_data(self, query={}, projection=None) :
        cursor = self.collection.find(query, projection)
        print(cursor)
        #DataFrame으로 변환
        return pd.DataFrame(list(cursor))
    
    def close_connetion(self) :
        self.client.close()