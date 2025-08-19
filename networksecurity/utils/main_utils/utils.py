import os
import sys
# import dill
import pickle
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import numpy as np

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        '''
        yaml.safe_load is used instead of yaml.load because:
            It is safer — avoids executing arbitrary Python code embedded in yaml
        '''
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace: # If replace is True,and file already exists,file is first deleted
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

def save_numpy_array_data(file_path:str,array:np.array):
    '''
    Save Numpy array data as file
    array -> np.array data to save
    file_path -> str location of file to save
    '''
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
    
def save_object(file_path:str,obj:object):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e