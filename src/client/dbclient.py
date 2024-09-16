from domain.model import PostgresConnection
from services.config.config import Config
import yaml

class DBClient:

    
    def getConnection(self, key: str) -> PostgresConnection:
        params = Config().getConfig()
        CONNECTION_PATH = params["CONNECTION_PATH"]
        with open(CONNECTION_PATH, 'r') as file:
            data = yaml.safe_load(file)[key]
        
        connetion = PostgresConnection(**data)
        return connetion