import logging
import os
from datetime import datetime
import os
import pandas as pd
import numpy as np
from thyroid import utils
from thyroid.logger import logging
from thyroid.exception import ThyroidException


from thyroid.logger import logging
from thyroid.utils import load_object
from thyroid.config import TARGET_COLUMN
from thyroid.entity import config_entity
from thyroid.predictor import ModelResolver
from thyroid.exception import ThyroidException
from thyroid.components.data_validation import DataValidation
from thyroid.entity.config_entity import DataValidationConfig


PREDICTION_DIR= "prediction"
VALIDATION_DIR= "validation_report"

validation_error=dict()


input_file_path = os.path.join("hypothyroid.csv")
base_file_path = os.path.join("hypothyroid.csv")

os.makedirs(PREDICTION_DIR,exist_ok=True)
report_file_dir = os.path.join(PREDICTION_DIR, VALIDATION_DIR)
os.makedirs(report_file_dir, exist_ok=True)
model_resolver = ModelResolver(model_registry="saved_models")     
df = pd.read_csv(input_file_path)
base_df= pd.read_csv(base_file_path)

df.replace({"?":np.NAN},inplace=True)
base_df.replace({"?":np.NAN},inplace=True)
        

df = model_resolver.feature_encoding(df=df)
exclude_columns = [TARGET_COLUMN]
utils.convert_columns_float(df=df, exclude_columns=exclude_columns)
df = model_resolver.handling_null_value_and_outliers(df=df)


      
knn_imputer = load_object(file_path=model_resolver.get_latest_knn_imputer_path())
        
        # Getting input features
input_feature_names =  list(knn_imputer.feature_names_in_)
        # data frame
input_arr = knn_imputer.transform(df[input_feature_names])

        # Prediction    
       
model = load_object(file_path=model_resolver.get_latest_model_path())
prediction = model.predict(input_arr)

        # Target decoding   
   
target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

cat_prediction = target_encoder.inverse_transform(prediction)

df["prediction"]=prediction
df["cat_pred"]=cat_prediction

        
# Creating file name for predition with time stamp by replacing .csv
prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        # Creating directory to save prediction file
prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        # Saving the df to directory
df.to_csv(prediction_file_path,index=False,header=True)

    

#log file name
LOG_FILE_NAME = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

#log directory
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")

#create folder if not available
os.makedirs(LOG_FILE_DIR,exist_ok=True)

#log file path

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
