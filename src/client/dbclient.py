from src.domain.model import PostgresConnection
import os
import yaml

class DBClient:

    
    def getConnection(self, key: str) -> PostgresConnection:
        
        CONNECTION_PATH = os.getenv("CONNECTION_PATH")
        with open(CONNECTION_PATH, 'r') as file:
            data = yaml.safe_load(file)[key]
        
        connetion = PostgresConnection(**data)
        return connetion