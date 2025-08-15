# 4 Steps will be involved in Data Ingestion -:
    # 1. Read from MongoDB
    # 2. Feature Store
    # 3. Split into Train and Test
    # 4. Save the Train and Test into Ingested

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)

            df.replace({"na":np.nan},inplace=True)
            return df
        

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            # Gets the file path (Artifacts/timestamp/data_ingestion/feature_store/phisingData.csv)
            dir_name=os.path.dirname(feature_store_file_path)
            # Extracts directory(folder)name from the path (/phisingData se pehle wala)
            os.makedirs(dir_name,exist_ok=True) # Makes that directory, no errors if already exists
            dataframe.to_csv(feature_store_file_path,index=False,header=True) # converts to csv and stores it in that path
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info('Performed train test split')
            
            dir_name=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_name,exist_ok=True)

            logging.info('Exporting train and test file path')

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            logging.info('Exported train and test file path')

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)