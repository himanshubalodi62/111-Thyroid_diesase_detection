import pymongo
import pandas as pd
import json
# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH="/config/workspace/hypothyroid.csv"
DATABASE_NAME="Healthcare"
COLLECTION_NAME="Thyroid"

if __name__=="__main__":
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and Columns:{df.shape}")

    #convert dataframe to json so that we can doump the record in mongodb. 
    df.reset_index(drop=True,inplace=True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])


    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)