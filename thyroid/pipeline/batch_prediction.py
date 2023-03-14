import os,sys
import pandas as pd
import numpy as np
from datetime import datetime

from thyroid import utils
from thyroid.logger import logging
from thyroid.utils import load_object
from thyroid.config import TARGET_COLUMN
from thyroid.entity import config_entity
from thyroid.predictor import ModelResolver
from thyroid.exception import ThyroidException
from thyroid.entity.config_entity import TARGET_ENCODER_OBJECT_FILE_NAME, MODEL_FILE_NAME, KNN_IMPUTER_OBJECT_FILE_NAME

PREDICTION_DIR= "prediction"


def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info("Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")   # Location where models are saved
        logging.info(f"Reading file :{input_file_path}")
        df = pd.read_csv(input_file_path)
        #base_df= pd.read_csv(base_file_path)
        logging.info("Replace '?' value to nan in base and input df")
        df.replace({"?":np.NAN},inplace=True)
        #base_df.replace({"?":np.NAN},inplace=True)
        #validation
    except Exception as e:
        raise ThyroidException(e, sys)   

#change the datatype
def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    """
    Converting column to float type except target column
    """
    try:
        obj_cols = df.columns[df.dtypes.eq('O')]
        obj_cols = df[obj_cols]
        for column in obj_cols.columns:
            if column not in exclude_columns:
                #df[column]=df[column].astype('float')
                #df[column] = df[column].apply(pd.to_numeric, errors='coerce') 
                df[column] = pd.to_numeric(column, errors='coerce') # ignore errors
        return df
    except Exception as e:
        raise ThyroidException(e, sys)
        # Loading knn_imputer
        logging.info("Loading knn imputer to get dataset")
        knn_imputer = load_object(file_path=model_resolver.get_latest_knn_imputer_path())
        
        # Getting input features
        input_feature_names =  list(knn_imputer.feature_names_in_)
        # data frame
        input_arr = knn_imputer.transform(df[input_feature_names])

        # Prediction    
        logging.info("Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        # Target decoding   
        logging.info("Target encoder to convert predicted column into categorical")
        target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

        cat_prediction = target_encoder.inverse_transform(prediction)

        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction

        logging.info('Creating prediction file with time stamp')
        # Creating file name for predition with time stamp by replacing .csv
        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        # Creating directory to save prediction file
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        # Saving the df to directory
        df.to_csv(prediction_file_path,index=False,header=True)

        return prediction_file_path

    except Exception as e:
        raise ThyroidException(e, sys)