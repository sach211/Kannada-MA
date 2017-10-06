# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 00:44:43 2016

@author: Sachi Angle
"""

f = open("/home/sachi/Documents/NLP/data/Fin/data_init1.csv", 'w+');
f.write('extra <fs af=\'Features\'>\n')
f1 = open('/home/sachi/Documents/NLP/data/data1', 'r');
buf = f1.read()
f.write(buf)
f1.close()

f2 = open('/home/sachi/Documents/NLP/data/data3', 'r');
buf = f2.read()
f.write(buf)
f2.close()

f3 = open('/home/sachi/Documents/NLP/data/data4', 'r');
buf = f3.read()
f.write(buf)
f3.close()

import os
l = os.listdir('/home/sachi/Documents/NLP/data/data2')
for fl in l:
    f4 = open(os.path.join('/home/sachi/Documents/NLP/data/data2', fl), 'r')
    buf = f4.read()
    f.write(buf)
    f4.close()
 
f.close()
