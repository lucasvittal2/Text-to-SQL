from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.domain.core import ApplicationCore
from src.domain.model import SQLGenBodyRequest
from src.services.llm.generation import OpenAITextGenerator
from src.services.llm.embeding import OpenAIEmbeddingGenerator
import logging
import os 



# Logging setup

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
APP_NAME = os.getenv("APP_NAME")

logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - [{APP_NAME}] - %(levelname)s:  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)

# Config API
text_generator = OpenAITextGenerator()
embedding_generator = OpenAIEmbeddingGenerator()
core = ApplicationCore(text_generator, embedding_generator)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

#Define API Endpoints

@app.post("/text-to-sql/generateSQL")
def generateSQL(body_request: SQLGenBodyRequest):
    try:
        sql_query = core.generateSQLQuery(question= body_request.question)
        response = JSONResponse( content= {"query": sql_query}, status_code= status.HTTP_200_OK)
    except:
        response = JSONResponse( content={"error_message" : "Failed to generate SQL query, contact the support."}, status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response


@app.get("/items/UpdateMetadataEmbeddings")
def updateEmbeddings():
    try:
        core.updateEmbeddings()
        response = JSONResponse( content= {"message": "Metdata Embedding were updated successfully !"}, status_code= status.HTTP_200_OK)
    except:
        response = JSONResponse( content={"error_message" : "Failed to update metadata embeddings, contact the support."}, status_code= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return response