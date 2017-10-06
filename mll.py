# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 04:45:57 2017

@author: Sachi Angle
"""

import pandas as pd
import pickle
import string
import Levenshtein as lv
#import matplotlib.mlab as mlab
#import seaborn as sb

d = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/data_io_fin.csv')
all_inputs = d[['cur_letter', 'root', 'noun', 'vowel', 'singular', 'd', 'prefix', 'cur_prefix']].values
all_classes = d['cur_seg'].values

from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
svc = SVC()

(training_inputs, testing_inputs, training_classes, testing_classes) = train_test_split(all_inputs, all_classes, train_size=0.75, random_state=0)       
svc.fit(training_inputs, training_classes)

"""
Accuracy check
xp, yp, pp
"""

x = []
y = []
p = []
data = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/data_io.csv')
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

count_total, count_correct = 0, 0
for i in range(len(testing_inputs)):
    print i
    correct = id_to_seg[testing_classes[i]]
    pred = svc.predict(testing_inputs[i])
    pred = id_to_seg[pred[0]]
    c_total = len(pred)
    if len(pred) < len(correct):
        c_total = len(correct)
    count_total = count_total + c_total
    count_correct = count_correct + (c_total - lv.distance(correct, pred))
    if correct != pred:
        x.append(id_to_letter[testing_inputs[i][0]])
        y.append(correct)
        p.append(pred)
    print '\n'
accuracy = (float(count_correct)/float(count_total)) * 100

average = 0
for i in range(len(testing_inputs)):
    print i
    correct = id_to_seg[testing_classes[i]]
    pred = svc.predict(testing_inputs[i])
    pred = id_to_seg[pred[0]]
    c_total = len(pred)
    if len(pred) < len(correct):
        c_total = len(correct)
    average = average + (float(c_total - lv.distance(correct, pred))/float(c_total))
    x.append(id_to_letter[testing_inputs[i][0]])
    y.append(correct)
    p.append(pred)
    print '\n'
accuracy = (float(average)/float(len(testing_inputs))) * 100



"""
filename = 'try1.sav'
sc = svc.score(testing_inputs, testing_classes)
pickle.dump(svc, open(filename, 'wb'))
print "Score: "
print sc

svc = pickle.load(open(filename, 'rb'))
sc = svc.score(testing_inputs, testing_classes)
print "Score: "
print sc

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
"""


"""
PREDICTING WORDS
out = ''
 r = 1
n = data.loc[pos]['noun']
sg = data.loc[pos]['sg_pl']
d = data.loc[pos]['d_o']
n = noun_to_id[n]
sg = sing_to_id[sg]
d = do_to_id[d]
pre = 0
cur = 0
for i in data.loc[pos]['in']:
    x = []
    x.append(letter_to_id[i])
    x.append(r)
    x.append(n)
    x.append(vowel_to_id[i])
    x.append(sg)
    x.append(d)
    x.append(pre)
    x.append(cur)  
    y = svc.predict(x)
    out = out + id_to_seg[y[0]]
    pre = pre * 10 + letter_to_id[i]
    cur = cur * 10 + letter_to_id[i]
    if out[-1] == '*':
        r = 0
        cur = 0
"""
