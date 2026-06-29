import pandas as pd  
import numpy as np
import sys

def load_file():
    try:
       pd.options.future.infer_string = True
       return pd.read_csv("Datasets/sample_dataset_cleaner.csv")
    except Exception as err:
        print(f"An error occured as {err}.Please try again.")
        sys.exit()
