from src.services.config.config import Config
from typing import List
from openai import OpenAI
import logging


class EmbeddingGenerator:
    
    def __init__(self, embedding_model:str, api_key: str) -> None:
        self.embedding_model = embedding_model
        self.api_key = api_key
        
        
    def getEmbedding(text:str) -> List[float]:
        raise NotImplemented("Method 'getEmbedding' were not implemented by 'EmbeddingGenerator' child")
    
    def __getParams(self) -> None:
        raise NotImplemented("Method '__getParams' were not implemented by 'EmbeddingGenerator' child")

class OpenAIEmbeddingGenerator(EmbeddingGenerator):
    
    def __init__(self) -> None:

        self.__getParams()
        self.client = OpenAI(api_key= self.api_key)
        
    def getEmbedding(self, text:str) -> List[float]:
        
        try:
            self.__getParams()
            embedding = self.client.embeddings.create(input = [text], model=self.embedding_model).data[0].embedding
            logging.info(f"The text {text}' were transformed to OpenAI embedding.")
            return embedding
        except Exception as err:
            logging.error(f"OpenAI embedding generation has failed due to the following error: \n\n{err}\n\n")
            raise err

    def __getParams(self) -> None:
        parms = Config().getConfig()
        embedding_model = parms["OPENAI_EMBEDDING_MODEL"]
        api_key= parms["OPENAI_KEY"]
        super().__init__(embedding_model, api_key )