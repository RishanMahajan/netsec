import os
import sys
import numpy as np
import pandas as pd

# Defining commom constant variables for training pipeline
TARGET_COLUMN='Result' # Self explanatory
PIPELINE_NAME:str='NetworkSecurity'
ARTIFACTS_DIR:str='Artifacts' # All generated files will be stored here
FILE_NAME:str='phisingData.csv' # Self explanatory

TRAIN_FILE_NAME:str='train.csv' # Self explanatory
TEST_FILE_NAME:str='test.csv' # Self explanatory


# Data Ingestion related constants
DATA_INGESTION_COLLECTION_NAME:str='NetworkData' # Collection Name
DATA_INGESTION_DATABASE_NAME:str='RishanAI' # Database Name
DATA_INGESTION_DIR_NAME:str="data_ingestion" # Main folder for ingestion related files.
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store" # Sub folder for clean,processed data
DATA_INGESTION_INGESTED_DIR:str="ingested" # Sub folder for final ingested data(train/test)
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2