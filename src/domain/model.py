from dataclasses import dataclass



@dataclass
class PostgresConnection:
    
    host:str
    database: str
    user: str
    password: str
    port: str