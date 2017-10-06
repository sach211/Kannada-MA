# -*- coding: utf-8 -*-
"""
Created on Sun Dec 04 01:30:17 2016

@author: Sachi Angle
"""

def utf2wx(inpchar):

##    import codecs
    f1=open('/home/sachi/Documents/NLP/NLP_PyScripts/unikannada.txt','r');
    unichar=f1.read();
    unichardecode = unichar.decode('utf-8');
    unicharinp = unichardecode[1:len(unichardecode)];
    uniline=unicharinp.splitlines();
    myunicodetable=[];
    for i in range(len(uniline)):
        mylist=uniline[i].split('\t');
        myunicodetable.append(mylist);
    f1.close();

    f2=open('/home/sachi/Documents/NLP/NLP_PyScripts/wxkannada.txt','r');
    wxchar=f2.read();
    wxcharinp = wxchar[0:len(wxchar)];
    wxline=wxcharinp.splitlines();
    mywxcodetable=[];
    for i in range(len(wxline)):
        mylist=wxline[i].split('\t');
        mywxcodetable.append(mylist);

    ## Store backspace character for 'Killer stroke'
    ## mywxcodetable[4][13]=u'\u0008';

    f2.close();


##    finp=open('sample.txt','r');
##    fout = codecs.open('test.txt', encoding='utf-8', mode='w+')
##    inpchar = finp.read();

    

    inpchardecode = inpchar.decode('utf-8');
    inpcharinp = inpchardecode[0:len(inpchardecode)];

    resstr="";
    for item in inpcharinp:
        found = 0;
        item
        if (item >= u'\u0c80' and item <= u'\u0cff'):
            diff=ord(item)-ord(u'\u0c80');
            j=diff % 16;
            i= diff // 16;
    ##        print i
    ##        print j
            if(item==myunicodetable[4][13]):
                resstr=resstr[0:len(resstr)-1];
            elif(item==myunicodetable[4][3] or item==myunicodetable[4][6] or item==myunicodetable[4][10] or item==myunicodetable[4][11] or item==myunicodetable[4][12] or item==myunicodetable[3][14] or item==myunicodetable[3][15] or item==myunicodetable[4][0] or item==myunicodetable[4][1] or item==myunicodetable[4][2] or item==myunicodetable[4][7] ): # eY,i
                resstr=resstr[0:len(resstr)-1];
                resstr=resstr+str(mywxcodetable[i][j].encode('utf-8'));
            elif(mywxcodetable[i][j]==''):
                print "Error in the Unicode: unknown unicode:"
                exit 
            else:
                resstr=resstr+str(mywxcodetable[i][j].encode('utf-8'));
        else:      
            resstr=resstr+item;
        ##mywxcodetable[i][j];

##    fout.write(resstr);
##    finp.close();
##    fout.close();
##    print resstr
    return resstr;






import pandas as pd

data = pd.read_csv('/home/sachi/Documents/NLP/data/Fin/data_1.csv')
data = data.drop('Unnamed: 0', 1)
data = data[['root', 'suffixes', 'suff-wx', 'word', 'noun', 'sg/pl', 'd/o']]

wxr = []
wxw = []
for i in data["root"]:
    wxc = utf2wx(str(i))
    wxr.append(wxc)
    
for i in data["word"]:
    wxc = utf2wx(str(i))
    wxw.append(wxc)
    
data['wx_root'] = wxr
data['wx_word'] = wxw

data.to_csv('/home/sachi/Documents/NLP/data/Fin/data_almost.csv', encoding = 'utf-8')
