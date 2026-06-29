import pandas as pd  
import numpy as np
import loader,cleaner,analyser,reporter,utils,sys

file = loader.load_file()
print('''1. View Dataset Summary\n
2. Analyze Missing Values\n
3. Detect Outliers\n
4. View Suggestions\n
5. Clean Dataset\n
6. Generate Report\n
7. Export Dataset\n
8. Exit\n''')

check = int(input("Please Enter a choice :- "))

if(check == 1):
    analyser.data_summary(file)

elif(check == 2):
    analyser.missing_values(file)