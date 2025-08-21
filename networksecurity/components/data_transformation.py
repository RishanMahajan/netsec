import sys
import os
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import KNNImputer

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(
            self,data_validation_artifact:DataValidationArtifact,
            data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame: # Reads the csv file and converts it into df
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_obj(cls)->Pipeline:
        # Initialises a KNN Imputer obj with params defined in training pipeline.py
        # and returns a pipeline obj with knn imputer as the first step
        logging.info('Entered get_data_transformer_obj of DataTransformation class')
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([('imputer',imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info('Entered data transformation method of transformation class')
        try:
            logging.info('Starting data transformation')
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            # Read train and test and converted from csv to df
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1, 0)
            # Split into x_train,y_train

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1, 0)
            # Split into x_test,y_test

            # KNN Imputer takes the nearest 3 neighbors (n_neighbors=3) and takes the avg
            # It then replaces np.nan with this avg
            preprocessor=self.get_data_transformer_obj()
            transformed_input_train_features=preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_features=preprocessor.transform(input_feature_test_df)
            # Preprocessed x_train,x_test

            train_arr=np.c_[transformed_input_train_features,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_features,np.array(target_feature_test_df)]
            # Combined both as a numpy array

            save_numpy_array_data(self.data_transformation_config.data_transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformed_test_file_path,array=test_arr)
            save_object(self.data_transformation_config.transformed_obj_file_path,preprocessor)
            save_object('final_model/preprocessor.pkl',preprocessor)
            # Preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_obj_file_path=self.data_transformation_config.transformed_obj_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)