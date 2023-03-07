from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator


with DAG(
    'thyroid_training', #its name of DAG
    default_args={'retries': 2}, # if first time this failed automatically its going to training 
    # [END default_args]
    description='Thyroid Disease Detection',
    schedule_interval="@weekly", #this pipeline is run weekly basis
    start_date=pendulum.datetime(2023, 3, 3, tz="UTC"), #this is a start date
    catchup=False,  #its relation of previouse one (its not required)
    tags=['example'],
) as dag:

    
    def training(**kwargs):  # here we define a function which we want to call
        from thyroid.pipeline.training_pipeline import start_training_pipeline
        start_training_pipeline()
    
    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")

    training_pipeline  = PythonOperator(
            task_id="train_pipeline",
            python_callable=training

    )

    sync_data_to_s3 = PythonOperator(
            task_id="sync_data_to_s3",
            python_callable=sync_artifact_to_s3_bucket

    )

    training_pipeline >> sync_data_to_s3