# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 04:45:57 2017

@author: Sachi Angle
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
#import seaborn as sb

d = pd.read_csv('D:\Projects\NLP\data\\data_io_fin.csv')
all_inputs = d[['curr_letter_id','vowel_id', 'prefix_word_id']].values
all_classes = d['segment'].values

from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
svc = SVC()

"""(training_inputs, testing_inputs, training_classes, testing_classes) = train_test_split(all_inputs, all_classes, train_size=0.75, random_state=1)       
    



svc.fit(training_inputs, training_classes)
sc = svc.score(testing_inputs, testing_classes)

"""
model_accuracies = []
for i in range(10):
    (training_inputs, testing_inputs, training_classes, testing_classes) = train_test_split(all_inputs, all_classes, train_size=0.75)
    svc.fit(training_inputs, training_classes)
    sc = svc.score(testing_inputs, testing_classes)
    model_accuracies.append(sc)

#sb.distplot(model_accuracies)
#n, bins, patches = plt.hist(model_accuracies, 50, normed=1, facecolor='green', alpha=0.75)

from sklearn.cross_validation import cross_val_score

cv_scores = cross_val_score(svc, all_inputs, all_classes, cv = 10)
#n, bins, patches = plt.hist(cv_scores, 50, normed=1, facecolor='green', alpha=0.75)
#sb.distplot(cv_scores)
#plt.title('Average score: {}'.format(np.mean(cv_scores))) 



    
    
    
    

