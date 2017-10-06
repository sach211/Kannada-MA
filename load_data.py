# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:26:55 2016

@author: Sachi Angle
"""

import numpy as np
import pandas as pd

data_temp = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/data_init1.csv', na_values = ['NA'], sep = "<fs af='");
Features = data_temp["Features'>"]
Features = np.array(Features)

modified_features = []
modified_features.append("root,noun,NaN,sg/pl,3,d/o,suffixes,suff-wx,word")
for i in Features:
    row = ""
    s = str(i)
    for j in range(len(s) - 1): 
        if s[j] == '\'' and s[j+1] == '>' :  
            continue
        elif s[j] != '>':
           row = row + s[j]
    row = row.replace("' name='", ",")
    modified_features.append(row)

f1 = open('/home/sachi/Documents/NLP/data/Fin/pre_data_features.csv', 'w');
for i in modified_features:
    f1.write(i)
    f1.write('\n')
f1.close();

data = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/pre_data_features.csv', error_bad_lines=False)
data = data[data["root"] != "None"]
data = data[data["noun"] != "punc"]
flag = []
for root in data["root"]:
    if str(root) == 'nan' or str(root) == 'Non':
        flag.append(False)
    else:
        flag.append(True)

data = data[flag]
data.to_csv('/home/sachi/Documents/NLP/data/Fin/final_data.csv')
