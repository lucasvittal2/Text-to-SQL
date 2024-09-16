from typing import List
from services.llm.embeding import EmbeddingGenerator
from services.config.config import Config
from database.postgres import PostgredDBHandler
from database.chroma import ChromaDBHandler, ChromaCollectionData
import logging
import json


class ApplicationCore:

    def __init__(self) -> None:
        self.config = Config()
        self.postgres = PostgredDBHandler()
        self.chroma = ChromaDBHandler()
        self.embedding_generator = EmbeddingGenerator()      

    def updateEmbeddings(self) -> None:
        
        self.__getParams()
        columns_metadata = self.__readJsonl("C:/Users/lucas/OneDrive/Documentos/projects/Text-to-SQL/assets/json/columns.jsonl")
        tables_metadata = self.__readJsonl("C:/Users/lucas/OneDrive/Documentos/projects/Text-to-SQL/assets/json/tables.jsonl")
        logging.info("Read metadata files.")
        columns_metadata_records = len(columns_metadata)
        tables_metadata_records = len(tables_metadata)
        logging.info("Generating embeddings...")
        columns_metadata_embeddings = [self.embedding_generator.getEmbedding(doc) for doc in columns_metadata ]
        tables_metadata_embeddings = [self.embedding_generator.getEmbedding(doc) for doc in columns_metadata ]

        col_ids = [str(idx) for idx in (1, columns_metadata_records + 1)]  
        tab_ids = [str(idx) for idx in (1, tables_metadata_records + 1)]  

        col_metadata_collection_data = ChromaCollectionData(ids = col_ids, embeddings = columns_metadata_embeddings, documents = columns_metadata)
        tab_metadata_collection_data = ChromaCollectionData(ids = tab_ids, embeddings = tables_metadata_embeddings, documents = tables_metadata)

        self.chroma.createCollection("columns", col_metadata_collection_data) 
        self.chroma.createCollection("tables", tab_metadata_collection_data)
        logging.info("Updated metadata successfully.")

    def __readJsonl(self, path: str) -> List[dict]:
        content = []
        with open(path, 'r') as file:
            for line in file.readlines():
                json_parssed = json.loads(line)
                content.append(json_parssed)
        return content


    def generateSQLQuery(self, question: str) -> str:
        
        attempt = 1
        while attempt <= self.MAX_ATTEMPTS:

            try:
                self.__getParams()
                logging.info(f"Trying to generate SQL query, Attempt {1} ...")
                most_sims_tables = self.chroma.getMostSimilars("tables", n_results=self.MAX_TABLE_METADATA_RECORDS, to_dict=True)
                cols_filter = {"$or": [ {"$contains": metadata["table_name"]} for metadata in most_sims_tables ] }
                most_sims_columns = self.chroma.getMostSimilars("columns", n_results=self.MAX_COLUMN_METADATA_RECORDS, filter= cols_filter)
                most_sims_tables = [json.dumps(metadata) for metadata in most_sims_tables]
                prompt = self.__buildPrompt(question, most_sims_tables, most_sims_columns)
                #generate text
                #validate text with running query
                logging.info("SQL query generated and validated sucessfully !")

            except Exception as err:

                logging.warning("The SQL generation process has failed, the validation didn't passed. Trying again...")
                attempt+=1

        logging.erro("SQL query generationg has failed, it was not possible to generate a valid SQL query")
        raise Exception("SQL query generationg has failed, it was not possible to generate a valid SQL query")
    
    def __getParams(self) -> None:
        params = self.config.getConfig()
        self.MAX_ATTEMPTS: int = params["MAX_ATTEMPTS"]
        self.MAX_TABLE_METADATA_RECORDS: int = params["MAX_TABLE_METADATA_RECORDS"]
        self.MAX_COLUMN_METADATA_RECORDS: int = params["MAX_COLUMN_METADATA_RECORDS"]
        self.BASE_PROMPT: str = params["BASE_PROMPT"]

    def __buildPrompt(self, question: str,column_metadata: List[str]) -> str:
        
        self.__getParams()
        str_column_metadata = "\n".join(column_metadata)
        prompt = self.BASE_PROMPT\
                    .replace("<QUESTION>", question)\
                    .replace("<MATCHED_SCHEMA>",str_column_metadata)
        return prompt

