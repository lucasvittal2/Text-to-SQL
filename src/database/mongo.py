from typing import List
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
import os
import logging

class MongoDBHandler:
    
    def __init__(self):
        
        uri = os.getenv("MONGO_URI")
        database_name = os.getenv("APP_DATABASE")
        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    def createCollection(self, collection_name: str):
        
        try:
            self.database.create_collection(collection_name)
            logging.info(f"Collection '{collection_name}' created successfully.")
        except CollectionInvalid:
            logging.warnning(f"Collection '{collection_name}' already exists, so the collection creation on MongoDB were aborted.")
        except Exception as err:
            logging.error(f"Collection creation on MongoDB has failed due to the following error: \n\n{err}\n\n")

    def getDocument(self, collection_name: str, query: dict):
        
        try:
            
            collection = self.database[collection_name]
            document = collection.find_one(query)
            logging.info("Got Da ocument from mongoDB")
            return document
        except Exception as err:
            
            logging.error(f"Getting document from mongoDB has failed due to the following error: \n\n{err}\n\n")
            raise err

    def upsertDocument(self, collection_name: str, query: dict, update_data: dict):
        
        try:
            collection = self.database[collection_name]
            result = collection.update_one(query, {'$set': update_data}, upsert=True)
            logging.info("Upserting operation on MongoDB has ben done successfully. ")
            
        except Exception as err:
            
            logging.error(f"Upserting operation has failed on MongoDB due to the followin error: \n\n{err}\n\n")
            raise err

    def deleteCollection(self, collection_name: str):
        try:
            
            collection = self.database[collection_name]
            collection.drop()
            logging.info(f"Collection '{collection_name}' deleted.")
        except Exception as err:
            
            logging.error(f"Deleting collection from mongoDB has failed due to the following error: \n\n{err}\n\n")
            raise err  
        

    def deleteDocuments(self, collection_name: str, query: dict):
        
        try:
            
            collection = self.database[collection_name]
            result = collection.delete_many(query)
            logging.info(f"Deleted {result.deleted_count} document(s) from collection '{collection_name}' on MongoDB.")
        
        except Exception as err:
            
            logging.error(f"Deleting Documens on collection '{collection_name}' from mongoDB has failed due to the following error: \n\n{err}\n\n")
            raise err  
            

    def insertDocuments(self, collection_name: str, documents: List[dict]):
        
        try:
            collection = self.database[collection_name]
            result = collection.insert_many(documents)
            logging.info(f"Inserted {len(result.inserted_ids)} document(s) in collection '{collection_name}' on MongoDB.")
            
        except Exception as err:
            
            logging.error(f"Inserting Documens on collection '{collection_name}' on mongoDB has failed due to the following error: \n\n{err}\n\n")
            raise err  
        
    def getCollectionData(self, collection_name: str) -> List[dict]:
        try:
            collection = self.database[collection_name]
            data = list(collection.find())
            logging.info(f"Got {len(data)} documents from collection '{collection_name}' fromMongoDB.")
            return data
            
        except Exception as err:
            
            logging.error(f"Inserting Documens on collection '{collection_name}' on mongoDB has failed due to the following error: \n\n{err}\n\n")
            raise err 