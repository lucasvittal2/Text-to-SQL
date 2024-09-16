import psycopg2
import pandas as pd
import logging
from domain.model import PostgresConnection


class PostgredDBHandler:
   
    
    def __init__(self, connection: PostgresConnection):

        self.connection = psycopg2.connect(
            host=connection.host,
            database=connection.database,
            user=connection.user,
            password=connection.password,
            port=connection.port
        )
        logging.info(f"Connected to '{connection.database} in PostgresDB.")

    def __enter__(self):

        self.client = self.connection.cursor()
        logging.info("session on PostgresDB were initiated !")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
    
        if self.client:
            self.client.close()
            logging.info("session on PostgresDB were finished !")

    def __del__(self):
        self.connection.close()
        logging.info("Connection on PostgresDB were closed !")


    def RunQuery(self, query: str):

        try:

            with self:
                self.client.execute(query)
                data = self.client.fetchall()
                table_data = pd.DataFrame(data)
                logging.info(f"Runned query. Got {len(table_data)}  records.")
            return table_data
        
        except Exception as err:
            logging.error(f"Query execution on PostgresDB has failed due to the foloowing error: \n\n{err}\n\n", exc_info=True)
            raise err
           
