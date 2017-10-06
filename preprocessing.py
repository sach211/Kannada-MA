# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 14:57:55 2016

@author: Sachi Angle
"""
import numpy as np
import pandas as pd

data = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/data_almost.csv')
data = data.drop('Unnamed: 0', 1)
data = data[['wx_word', 'wx_root', 'suff-wx', 'noun', 'sg/pl', 'd/o']]

for col in data.columns:
    data[col].loc[data[col].isnull()] = '0'

root = []
for word in data['wx_root']:
    x = word.find('\xe2\x80\x8c')
    if x == -1:
        root.append(word)
    else:
        sx = ""
        for c in range(len(word)):
            if c >= x and c < x + 3:
                continue
            sx = sx + word[c]
        root.append(sx)

suff = []
for word in data['suff-wx']:
    x = word.find('\xe2\x80\x8c')
    if x == -1:
        suff.append(word)
    else:
        sx = ""
        for c in range(len(word)):
            if c >= x and c < x + 3:
                continue
            sx = sx + word[c]
        suff.append(sx)
        
vowel = ['a', 'e', 'i', 'o', 'u']
cvform = []
for word in data['wx_word']:
    s = ""
    for c in str(word):
        s = s + c + '-'
        if c in vowel:
            s = s + 'V '
        else:
            s = s + 'C '
    s = s[:-1]
    cvform.append(s)
data['cv_word'] = cvform

cvform = []
for word in root:
    s = ""
    for c in word:
        s = s + c + '-'
        if c in vowel:
            s = s + 'V '
        else:
            s = s + 'C '
    cvform.append(s)
data['cv_root'] = cvform

cvform = []
for word in suff:
    if word == '0':
        cvform.append('0')
    elif str(word) == 'nan':
        cvform.append(word)
    else:
        s = ""
        for c in word:
            s = s + c
            if c in vowel:
                s = s + '-V '
            elif c != '+':
                s = s + '-C '
        cvform.append(s)
data['cv_suffixes'] = cvform

segmented = []
words = []

def split(word):
    w = ""
    for i in str(word):
        w += i
        w += ' '
    w = w[:-1]
    words.append(w)
    
def align(t, word, s, i, j):
    if i == len(word) and j == len(s):
        t = t[:-1]
        segmented.append(t)
        return 1
    elif i == len(word) and j != len(s):
        if j + 1 == len(s):
            t = t[:-1]
            t += s[j]
            segmented.append(t)
            return 1
        else:
            return 0
    elif j == len(s) and i != len(word):
        if i + 1 == len(word):
            t += '$'
            segmented.append(t)
            return 1
        else:
            return 0
    if s[j] == '*' or s[j] == '+':
        t = t[:-1]        
        t += '*' + ' '
        return align(t, word, s, i, j + 1)
    elif s[j] == word[i]:
        t += s[j] + ' '
        return align(t, word, s, i + 1, j + 1)
    elif ((i + 1 < len(word)) and (word[i + 1] == s[j])) and (((j + 1 < len(s)) and (s[j + 1] == word[i])) or ((j + 2 < len(s)) and (s[j + 1] == '*' or s[j + 1] == '+') and (s[j + 2] == word[i]))):
        t1 = t
        t2 = t
        t1 += '$' + ' '
        a1 = align(t1, word, s, i + 1, j)
        if len(t) > 1 and t2[-2] != '*':
            t2 = t2[:-1]
            t2 += s[j] + ' '
        else:
            t2 += s[j]
        a2 = align(t2, word, s, i, j + 1)
        if a1 == 1 and a2 == 1:
            del segmented[-2:]
            return 5
        elif a1 == 1 or a2 == 1:
            return 1
        else:
            return 0
    elif (i + 1 < len(word)) and (word[i + 1] == s[j]):
        t += '$' + ' '
        return align(t, word, s, i + 1, j)
    elif ((j + 1 < len(s)) and (s[j + 1] == word[i])) or ((j + 2 < len(s)) and (s[j + 1] == '*' or s[j + 1] == '+') and (s[j + 2] == word[i])):
        if len(t) > 1 and t[-2] != '*':
            t = t[:-1]        
            t += s[j] + ' '
        else:
            t += s[j]
        return align(t, word, s, i, j + 1)
    else:
        return 0
        
def align2(t, word, s, i, j, f):
    if i == len(word) and j == len(s):
        t = t[:-1]
        segmented.append(t)
        return 1
    elif i == len(word) and j != len(s):
        if j + 1 == len(s):
            t = t[:-1]
            t += s[j]
            segmented.append(t)
            return 1
        else:
            return 0
    elif j == len(s) and i != len(word):
        if i + 1 == len(word):
            t += '$'
            segmented.append(t)
            return 1
        else:
            return 0
    if s[j] == '*' or s[j] == '+':
        t = t[:-1]        
        t += '*' + ' '
        return align2(t, word, s, i, j + 1, f)
    elif s[j] == word[i]:
        t += s[j] + ' '
        return align2(t, word, s, i + 1, j + 1, f)
    elif ((i + 1 < len(word)) and (word[i + 1] == s[j])) and (((j + 1 < len(s)) and (s[j + 1] == word[i])) or ((j + 2 < len(s)) and (s[j + 1] == '*' or s[j + 1] == '+') and (s[j + 2] == word[i]))):
        t1 = t
        t2 = t
        t1 += '$' + ' '
        a1 = align2(t1, word, s, i + 1, j, 1)
        if len(t) > 1 and t2[-2] != '*':
            t2 = t2[:-1]
            t2 += s[j] + ' '
        else:
            t2 += s[j]
        a2 = align2(t2, word, s, i, j + 1, 1)
        if a1 == 1 and a2 == 1:
            del segmented[-2:]
            return 5
        elif a1 == 1 or a2 == 1:
            return 1
        else:
            return 0
    elif (i + 1 < len(word)) and (word[i + 1] == s[j]):
        t += '$' + ' '
        return align2(t, word, s, i + 1, j, f)
    elif ((j + 1 < len(s)) and (s[j + 1] == word[i])) or ((j + 2 < len(s)) and (s[j + 1] == '*' or s[j + 1] == '+') and (s[j + 2] == word[i])):
        if len(t) > 1 and t[-2] != '*':
            t = t[:-1]        
            t += s[j] + ' '
        else:
            t += s[j]
        return align2(t, word, s, i, j + 1, f)
    else:
        if f == 1:
            return 0
        else:
            if len(t) > 1 and t[-2] != '*':
                t = t[:-1]        
                t += s[j] + ' '
            else:
                t += s[j]
            return align2(t, word, s, i, j + 1, f)            
            
err_list = []
E = []

for k in range(len(data["wx_root"])):
    s = ""
    s = root[k]
    if '0' != suff[k]:
        s += "*" + suff[k]
    t = ""
    word = str(data.loc[k]["wx_word"])
    split(word)
    flag = align(t, word, s, 0, 0) 
    if flag is 5:
        words = words[:-1]
        err_list.append(k)
    elif flag is 0:
        #E.append(k)
        #words = words[:-1]
        t = ""
        flag2 = align2(t, word, s, 0, 0, 0)
        if flag2 == 0:
            E.append(k)
            words = words[:-1]
        elif flag2 == 5:
            words = words[:-1]
            err_list.append(k)
        
          
words = pd.DataFrame(words)
uni_err = [47041, 66340, 67573, 68390, 72151, 72384, 73693, 75379, 82985, 87253, 87301, 88647]

segmented = [j for i, j in enumerate(segmented) if i not in (uni_err)]
inpt = [j for i, j in enumerate(data["wx_word"]) if i not in (E + err_list)]
inpt = [j for i, j in enumerate(inpt) if i not in (uni_err)]
inp = []
for i in range(len(inpt)):
    s = ""
    for c in inpt[i]:
        s = s + c + " "
    s = s[:-1]
    inp.append(s)
    
noun = [j for i, j in enumerate(data["noun"]) if i not in (E + err_list)]
noun = [j for i, j in enumerate(noun) if i not in (uni_err)]
sg_pl = [j for i, j in enumerate(data["sg/pl"]) if i not in (E + err_list)]
sg_pl = [j for i, j in enumerate(sg_pl) if i not in (uni_err)]
d_o = [j for i, j in enumerate(data["d/o"]) if i not in (E + err_list)]
d_o = [j for i, j in enumerate(d_o) if i not in (uni_err)]

io = pd.DataFrame({'in' : inpt, 'label' : segmented, 'noun' : noun, 'sg_pl' : sg_pl, 'd_o' : d_o}, columns=['in','label', 'noun', 'sg_pl', 'd_o'])

io.to_csv('/home/sachi/Documents/NLP/data/Fin/data_io.csv', encoding = 'utf-8')
