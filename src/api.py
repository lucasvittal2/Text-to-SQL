from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

APP_NAME = os.getenv("APP_NAME")
log_dir = "assets/logs"
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - [{APP_NAME}] - %(levelname)s: %(message)s',  # Use f-string corretamente
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(f"{log_dir}/app.log"),
        logging.StreamHandler()
    ]
)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


@app.get("/text-to-sql/generateSQL")
def generateSQL():
    return {"message": "generated sql!"}


@app.get("/items/UpdateMetadataEmbeddings")
def updateEmbeddings():
    return {"message": "Updated embeddings metadata !"}