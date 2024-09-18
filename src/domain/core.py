from src.services.llm.embeding import EmbeddingGenerator
from src.services.llm.generation import TextGenerator
from src.services.config.config import Config
from src.client.dbclient import DBClient
from src.database.postgres import PostgredDBHandler
from src.database.chroma import ChromaDBHandler, ChromaCollectionData
from typing import List
import logging
import json


class ApplicationCore:

    def __init__(self, text_generator: TextGenerator, embedding_generator: EmbeddingGenerator) -> None:

        self.__getParams()
        self.chroma = ChromaDBHandler()
        self.db_client = DBClient()
        connection = self.db_client.getConnection(self.CONNECTION_KEY)
        self.postgres = PostgredDBHandler(connection)
        self.embedding_generator = embedding_generator
        self.text_generation = text_generator    

    def updateEmbeddings(self) -> None:
        
        self.__getParams()
        columns_metadata = self.__readJsonl("./assets/json/columns.jsonl")
        tables_metadata = self.__readJsonl("./assets/json/tables.jsonl")
        logging.info("Reading metadata files...")
        logging.info(f"found {len(columns_metadata)} columns metadata records")
        logging.info(f"found {len(tables_metadata)} tables metadata records")
        columns_metadata_records = len(columns_metadata)
        tables_metadata_records = len(tables_metadata)
        
        logging.info("Generating embeddings...")

        columns_metadata_embeddings = [self.embedding_generator.getEmbedding(doc) for doc in columns_metadata ]
        tables_metadata_embeddings = [self.embedding_generator.getEmbedding(doc) for doc in tables_metadata ]

        col_ids = [str(idx) for idx in range(1, columns_metadata_records + 1)]  
        tab_ids = [str(idx) for idx in range(1, tables_metadata_records + 1)]  

        col_metadata_collection_data = ChromaCollectionData(ids = col_ids, embeddings = columns_metadata_embeddings, documents = columns_metadata)
        tab_metadata_collection_data = ChromaCollectionData(ids = tab_ids, embeddings = tables_metadata_embeddings, documents = tables_metadata)

        self.chroma.createCollection("columns", col_metadata_collection_data) 
        self.chroma.createCollection("tables", tab_metadata_collection_data)
        logging.info("Updated metadata successfully.")

    def __readJsonl(self, path: str, to_dict=False) -> List[dict]:
        content = []
        with open(path, 'r') as file:
            content = [json.loads(line) if to_dict else line for line in file.readlines()]
        return content


    def generateSQLQuery(self, question: str) -> str:
        
        attempt = 1
        while attempt <= self.MAX_ATTEMPTS:

            try:
                self.__getParams()
                logging.info(f"Trying to generate SQL query, Attempt {attempt} ...")
                most_sims_tables = self.chroma.getMostSimilars("tables", question, n_results=self.MAX_TABLE_METADATA_RECORDS, to_dict=True)
                
                cols_filter = {"$or": [ {"$contains": metadata["table_name"]} for metadata in most_sims_tables ] }
                most_sims_columns = self.chroma.getMostSimilars("columns", question, n_results=self.MAX_COLUMN_METADATA_RECORDS, filter= cols_filter)
                prompt = self.__buildPrompt(question, most_sims_columns)
                sql_query = self.text_generation.generateText(prompt)
                #self.postgres.RunQuery(sql_query)
            
                logging.info("SQL query generated and validated sucessfully !")
                return sql_query

            except Exception as err:

                logging.warning(f"\n\nThe SQL generation process has failed, the validation didn't passed due to the following exception : {err}\n\n",)
                logging.info("Trying Again...")
                attempt+=1

        logging.error("\n\nSQL query generationg has failed, it was not possible to generate a valid SQL query", exc_info=True)
        raise Exception("SQL query generationg has failed, it was not possible to generate a valid SQL query")
    
    def __getParams(self) -> None:

        config = Config()
        params = config.getConfig()
        self.MAX_ATTEMPTS: int = params["MAX_ATTEMPTS"]
        self.MAX_TABLE_METADATA_RECORDS: int = params["MAX_TABLE_METADATA_RECORDS"]
        self.MAX_COLUMN_METADATA_RECORDS: int = params["MAX_COLUMN_METADATA_RECORDS"]
        self.BASE_PROMPT: str = params["BASE_PROMPT"]
        self.CONNECTION_KEY = params["CONNECTION_KEY"]

    def __buildPrompt(self, question: str,column_metadata: List[str]) -> str:

        self.__getParams()
        str_column_metadata = "\n".join(column_metadata)
        prompt = self.BASE_PROMPT\
                    .replace("<QUESTION>", question)\
                    .replace("<MATCHED_SCHEMA>",str_column_metadata)
        return prompt

