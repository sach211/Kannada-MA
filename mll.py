# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 04:45:57 2017

@author: Sachi Angle
"""
from string import ascii_lowercase
import numpy as np 
import pandas as pd

cv = np.zeros(27)
vowel = ['a', 'e', 'i', 'o', 'u']
for i, c in enumerate(ascii_lowercase):
    if c in vowel:
        cv[i + 1] = 1
    
wa = []
wn = []
for i, c in enumerate(ascii_lowercase):
    wa.append(c)
    wn.append(i + 1)
word_id_alph = dict(zip(wa, wn))

data = pd.read_csv('D:\Projects\NLP\data\\data_io.csv')
data = data.drop('Unnamed: 0', 1)

unmatch = []       
for i in range(len(data)):   
    cc = 0    
    for ch in data.loc[i]['label']:
        if ch == ' ':            
            cc = cc + 1
    cc = cc + 1    
    if cc != len(data.loc[i]['in']):       
        unmatch.append(i)

segmented = [j for i, j in enumerate(data['label']) if i not in (unmatch)]
inpt = [j for i, j in enumerate(data['in']) if i not in (unmatch)]

curr_segment = []
root = []
prefix_seg = []
prefix_word = []

for word in segmented:
    s = ""
    sp = ""
    r = 1
    for char in word:
        if char == ' ':
            curr_segment.append(s)
            root.append(r)
            prefix_seg.append(sp[:-len(s)])
            if s[-1] == '*':
                r = 0
            s = ""
        else:
            s += char
            sp += char
    curr_segment.append(s)
    root.append(r)
    prefix_seg.append(sp[:-len(s)])
    
for word in inpt:
    s = ""
    for char in word:
        prefix_word.append(s)
        s += char
        
from sklearn.feature_extraction.text import CountVectorizer
        
vect = CountVectorizer(min_df=1)
    
    
    
    
    
    
    

