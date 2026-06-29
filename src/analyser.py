import pandas as pd  
import numpy as np

def data_summary(x):
    print(f"Rows :- {x.shape[0]}\nColumns :- {x.shape[1]}")
    print(x.dtypes)

def missing_values(x):
    nan_counts = x.isna().sum()
    print(nan_counts)
    duplicates = x[x.duplicated()]
    duplicate = x.duplicated().sum()
    print("\nNumber of Duplicate rows:", duplicate)
    return nan_counts,duplicates

