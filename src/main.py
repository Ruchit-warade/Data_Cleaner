import pandas as pd  
import numpy as np
import loader,cleaner,analyser,reporter,utils,sys

file = loader.load_file()
file_new = file.drop_duplicates()
print('''1. View Dataset Summary
2. Analyze Missing Values
3. Classify Columns      
4. Detect Outliers
5. View Suggestions
6. Clean Dataset
7. Generate Report
8. Export Dataset
9. Exit''')

check = int(input("Please Enter a choice :- "))

if(check == 1):
    analyser.data_summary(file)

elif(check == 2):
    analyser.missing_values(file)

elif(check == 3):
    analyser.column_seg(file_new)