import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from typing import List
import os
import logging
from dataclasses import dataclass

@dataclass
class ChromaCollectionData:
    ids: List[str]
    embeddings: List[float]
    documents: List[str]

class ChromaDBHandler:
    
    def __init__(self):
        print(os.getenv("CHROMADB_HOST"))
        self.client = chromadb.HttpClient(
            host=os.getenv("CHROMADB_HOST"),
            port=os.getenv("CHROMADB_PORT")
        )
        logging.info("Connected to ChromDB Client !")
        
    
        
    def createCollection(self,name: str, data: ChromaCollectionData) -> None:
        try:
            self.__getParams()
            logging.info(f"Creating collection '{name}'...")
            existent_collections = [collection.name for collection in self.client.list_collections()]
            logging.info(f"There are the following collection on ChromaDB: {existent_collections}")
            
            if name in existent_collections:
                self.client.delete_collection(name)
                logging.info(f"Collection '{name}' were found, it was excluded from chroma database.")
            
            
            self.client.create_collection(name, embedding_function=self.embedding_function)
            collection = self.client.get_collection(name)
            collection.add(
                ids=data.ids,
                embeddings= data.embeddings,
                documents = data.documents
            )
            logging.info(f"Collection '{name}' were created successfully !")
        except Exception as err:
            logging.error(f"Collection creating on ChromaDB has failed due the folloing error: \n\n{err}\n\n")
            raise err
        
    def getMostSimilars(self, collection_name:str, question: str, filter: List[dict] =None, n_results=10 )-> List[dict]:
        try:
            self.__getParams()
            collection = self.client.get_collection(collection_name, embedding_function=self.embedding_function)
            most_sims = collection.query(query_texts= question, where_document=filter, n_results=n_results)
            logging.info(f"Got {len(most_sims)} records from '{collection_name}'")
            return  most_sims
        except Exception as err:
            logging.error(f"Semanthic search on ChromaDB has failed due the folloing error: \n\n{err}\n\n")
            raise err
    
    def __getParams(self)->None:
        self.embedding_function = OpenAIEmbeddingFunction(api_key=os.environ.get('OPENAI_API_KEY'), model_name='text-embedding-3-small')
   