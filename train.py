from thyroid.pipeline.training_pipeline import start_training_pipeline


input_file_path="/config/workspace/hypothyroid.csv"

if __name__=="__main__":
    try:
        start_training_pipeline()
    except Exception as e:
        print(e)