# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 13:19:19 2016

@author: Sachi Angle
"""

import pandas as pd

data = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/final_data.csv')
data = data.drop('Unnamed: 0', 1)

for i in range(len(data)):
    if str(data.loc[i]["suff-wx"]) == 'nan':
        data.loc[i]["suff-wx"] = '0'
        
n = []
y = []
for i in range(len(data["suff-wx"])):
    if data.loc[i]["suff-wx"].find('\'') > -1:
        n.append(i)
    else:
        y.append(i)
        
data_spare = data.loc[n][:]
data = data.loc[y][:]

data.to_csv('/home/sachi/Documents/NLP/data/Fin/data_1.csv')
data_spare.to_csv('/home/sachi/Documents/NLP/data/Fin/data_2.csv')
