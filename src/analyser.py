import pandas as pd  
import numpy as np
import pandas.api.types as pdty
import re,math,tqdm

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

def type_bool(column,dict,x):
    type_bool = pdty.is_bool_dtype(x[column])
    if(type_bool == True):
        dict["Boolean"] = dict.get("Boolean") + 60

def type_float(column,dict,x):
    type_float = pdty.is_float_dtype(x[column])
    if(type_float == True):
        dict["Numeric"] = dict.get("Numeric") + 60

def type_int(column,dict,x):
    type_int = pdty.is_integer_dtype(x[column])
    if(type_int == True):
        dict["Numeric"] = dict.get("Numeric") + 50
        dict["Identifier"] = dict.get("Identifier") + 10        

def word_find(word,text):
    return bool(re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE))

def column_name(column,dict):
    if(word_find("id|roll|nvoice|customer",column) == True):
        dict["Identifier"] = dict.get("Identifier") + 50
    elif(word_find("age|salary|marks|price|height",column) == True) :
        dict["Numeric"] = dict.get("Numeric") + 50
    elif(word_find("country|state|gender",column) == True):
        dict["Categorical"] = dict.get("Categorical") + 50    
    elif(word_find("email",column) == True):
        dict["Email"] = dict.get("Email") + 50
    elif(word_find("date|dob|joined",column) == True):
        dict["Date"] = dict.get("Date") + 50
    elif(word_find("name",column) == True):
            dict["Name"] = dict.get("Name") + 50
    elif(word_find("review|feedback|comment",column) == True):
            dict["Text"] = dict.get("Text") + 50
    elif(word_find("active|married|passed",column) == True):
        dict["Boolean"] = dict.get("Boolean") + 50

def is_datetime(value):
    return pd.notna(pd.to_datetime(value, errors="coerce"))

def number_date(column,dict,x):
    list = []
    date  = []
    for i in x[column].tolist(): 
        date.append(is_datetime(i))      
        try:
            num = float(i)
            # Reject NaN and infinity
            list.append(math.isfinite(num))
        except (ValueError, TypeError):
            list.append(False)
    arr = np.array(list)        
    num_per = arr.mean()  # Mean of booleans = proportion of True
    if(num_per >= 0.95):
        dict["Numeric"] = dict.get("Numeric") + 40 
    list.clear()    
    date_ = np.array(date)
    date_per = date_.mean()
    if (date_per >= 0.95):
        dict["Date"] = dict.get("Date") + 50
    date.clear()

def email(column,dict,x):
    email = []
    for i in x[column].tolist():
        email.append(word_find("@", str(i)))
    email_  = np.array(email)
    email_per = email_.mean()
    if(email_per >= 0.95):
        dict["Email"] = dict.get("Email") + 60
    email.clear()

def unique(column,dict,x):
    unique_values = set()
    for i in x[column].tolist():
        unique_values.add(str(i).lower())
    if(len(unique_values) == 2):
        dict["Boolean"] = dict.get("Boolean") + 60
        dict["Categorical"] = dict.get("Categorical") + 10
    if(len(unique_values) <= x.shape[0]/10) :
        dict["Categorical"] = dict.get("Categorical") + 40
    if(x[column].is_unique):
        dict["Identifier"] = dict.get("Identifier") + 40
        dict["Email"] = dict.get("Email") + 10
        dict["Name"] = dict.get("Name") + 10
        dict["Text"] = dict.get("Text") + 10

    length = []
    for i in x[column].tolist():
        if(len(str(i)) >= 25):
            length.append(True)
        else:
            length.append(False)
    length_ = np.array(length)
    length_per  = length_.mean()
    if(length_per >= 0.95):
        dict["Text"] = dict.get("Text") + 60      

def column_seg(x):
    column_list = x.columns.tolist()
    category = {}
    scores = {"Identifier": 0,"Numeric": 0,"Categorical": 0,"Date": 0,"Boolean" : 0,"Email" : 0,"Name" : 0,"Text" : 0}
    for i in tqdm.tqdm(column_list):
        type_bool(i,scores,x)
        type_float(i,scores,x)
        type_int(i,scores,x)
        column_name(i,scores)
        number_date(i,scores,x)
        email(i,scores,x)
        unique(i,scores,x)
        category[i] = ("Unknown" if all(v == 0 for v in scores.values()) else max(scores, key=scores.get))
        scores = dict.fromkeys(scores, 0)
    print(pd.DataFrame([category]))