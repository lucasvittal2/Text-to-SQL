from dataclasses import dataclass
from pydantic import BaseModel



@dataclass
class PostgresConnection:
    
    host:str
    database: str
    user: str
    password: str
    port: str

class SQLGenBodyRequest(BaseModel):
    question: str
    