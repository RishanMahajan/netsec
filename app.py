import os
import sys

import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv('MONGODB_URL_KEY')
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
'''
FastAPI is the web framework.

Uvicorn is the server that runs FastAPI
'''
from fastapi import FastAPI,File,Request,UploadFile
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME

from fastapi.templating import  Jinja2Templates
templates=Jinja2Templates(directory='./templates') 
# Picks up all the hmtl files from templates folder
# Jinja2 = a way to merge Python values into HTML files,so you can render dynamic pages

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Any HTTP method (GET, POST, etc.) is allowed.
    allow_headers=['*']
)

'''
Asynchronous functions don’t block the event loop while waiting for something slow (like database calls, file I/O, API requests).

Instead, the server can handle other requests while waiting.

Even though your run_pipeline() looks like a CPU-heavy task (ML training), 
making it async means FastAPI can still accept other incoming requests while training is happening.
'''
@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get('/train')
async def train_model():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response('Training is successful')
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post('/predict')
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object('final_model\preprocessor.pkl')
        final_model=load_object('final_model\model.pkl')
        network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        print(y_pred)
        df['prediction column']=y_pred
        print(df['prediction column'])
        df.to_csv('prediction_output/output.csv')
        table_html=df.to_html(classes='table table-striped')
        return templates.TemplateResponse('table.html',{'request':request,'table':table_html})

    except Exception as e:
        raise NetworkSecurityException(e,sys)


if __name__=='__main__':
    app_run(app,host='localhost',port=8000)


# https://chatgpt.com/share/68a792c2-3cf4-800c-b151-f1b9a919760f