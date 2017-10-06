#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 14:47:41 2017

@author: sachi
"""

import pandas as pd
import string

data = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/data_io.csv')
data = data.drop('Unnamed: 0', 1)

len_bool = []
for index in range(len(data)):
    row = data.loc[index]
    count = 0
    for c in row['label']:
        if c == ' ':
            count = count + 1
    count = count + 1
    if count == len(row['in']):
        rowb = True
    else:
        rowb = False
    len_bool.append(rowb)        
    
data = data[len_bool].reset_index()

cur_letter = []
cur_seg = []
prefix = []
cur_prefix = []
root = []
vowel = []
noun = []
singular = []
d = []

key = []
value = []
key = list(string.ascii_letters) + ['0', '1', '2', '3', '4', '5', '6', '7','8', '9']
value = range(62)
count = 62
for word in data['in']:
    for letter in word:
        if letter not in key:
            key.append(letter)
            value.append(count)
            count = count + 1
letter_to_id = dict(zip(key, value))
id_to_letter = dict(zip(value, key))

value = [0]*len(letter_to_id)
vowel_to_id = dict(zip(key, value))
for letter in key:
    if letter in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
        vowel_to_id[letter] = 1
    elif letter in ['0', '1', '2', '3', '4', '5', '6', '7','8', '9']:
        vowel_to_id[letter] = 2
    elif letter not in list(string.ascii_letters):
        vowel_to_id[letter] = 3

key = []
value = []
count = 0
for i in range(len(data)):
    seg_label = data.loc[i]['label'].split(' ')
    for seg in seg_label:
        if seg not in key:
            key.append(seg)
            value.append(count)
            count = count + 1
seg_to_id = dict(zip(key, value))
id_to_seg = dict(zip(value, key))

key = []
value = []
count = 1
for n in data['noun']:
    if n not in key:
        key.append(n)
        value.append(count)
        count = count + 1
noun_to_id = dict(zip(key, value))
id_to_noun = dict(zip(value, key))

key = []
value = []
count = 1
for s in data['sg_pl']:
    if s not in key:
        key.append(s)
        value.append(count)
        count = count + 1
sing_to_id = dict(zip(key, value))
id_to_sing = dict(zip(value, key))

key = []
value = []
count = 1
for do in data['d_o']:
    if do not in key:
        key.append(do)
        value.append(count)
        count = count + 1
do_to_id = dict(zip(key, value))
id_to_do = dict(zip(value, key))

for i in range(len(data)):
    row = data.loc[i]
    n = row['noun']
    sp = row['sg_pl']
    do = row['d_o']
    seg_label = row['label'].split(' ')
    pre = 0
    cur_pre = 0
    r = 1
    for idx in range(len(seg_label)):
        cur_letter.append(letter_to_id[row['in'][idx]])
        cur_seg.append(seg_to_id[seg_label[idx]])
        noun.append(noun_to_id[n])
        singular.append(sing_to_id[sp])
        d.append(do_to_id[do])
        vowel.append(vowel_to_id[row['in'][idx]])
        prefix.append(pre)
        pre = pre * 10 + letter_to_id[row['in'][idx]]
        cur_prefix.append(cur_pre)
        cur_pre = cur_pre * 10 + letter_to_id[row['in'][idx]]
        root.append(r)
        if seg_label[idx][-1] == '*':
            r = 0
            cur_pre = 0
            
data_fin = pd.DataFrame({'cur_letter' : cur_letter, 'root' : root, 'noun' : noun, 'vowel' : vowel, 'singular' : singular, 'd' : d, 'prefix' : prefix, 'cur_prefix' : cur_prefix, 'cur_seg' : cur_seg}, columns=['cur_letter', 'root', 'noun', 'vowel', 'singular', 'd', 'prefix', 'cur_prefix', 'cur_seg'])
data_fin.to_csv('/home/sachi/Documents/NLP/data/Fin/data_io_fin.csv', encoding = 'utf-8')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    