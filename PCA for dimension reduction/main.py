# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 21:40:45 2018

@author: Jason
"""

import numpy as np
import time
#from sklearn.datasets import load_svmlight_file
from svmutil import *
from svm import *
from sklearn.preprocessing import StandardScaler,scale
from sklearn.cross_validation import cross_val_score
from sklearn.datasets import dump_svmlight_file
from sklearn.metrics import accuracy_score,precision_recall_fscore_support
from sklearn.svm import SVC
from scipy.linalg import eigh
import sys

#start = time.clock()

filename = str(sys.argv[1])
#filename = 'dataset4_sample.txt'
#feature_no = 126

s = filename.split('.')[0]
filename_out = s + '_out.txt'
data_y,data_x = svm_read_problem(filename)


data_y = np.array(data_y)
if str('1') in s:
    feature_no = 68
if str('2') in s:
    feature_no = 123
if str('3') in s:
    feature_no = 256
if str('4') in s:
    feature_no = 126


#data_x = np.array(data_x)
#standard_x = StandardScaler().fit_transform(data_x)
#totable = np.array([[key,val] for (key,val) in data_x[0].items()])
sample_x = []
for it in data_x:
    tmp = np.zeros(feature_no)
    try:
        for key in it.keys():
            tmp[key-1] = it[key]
    except:
        pass
    sample_x.append(tmp)
sample_x = np.array(sample_x)

#a = 0
#b = 0
##c = 0
#tmp = 0
#f_a = []
#f_b = []
##f_c = []
#for y in data_y:
#    if(y == -1):
#        a = a + 1
#        f_a.append(sample_x[tmp])
#    if(y == 1):
#        b = b + 1
#        f_b.append(sample_x[tmp])
##    if(y == 1):
##        c = c + 1
##        f_c.append(sample_x[tmp])
#    tmp = tmp + 1
#
#m_abc = min(a,b)
#f_a = np.array(f_a)
#f_b = np.array(f_b)
##f_c = np.array(f_c)
##sam_x = np.vstack((np.vstack((f_a[0:m_abc],f_b[0:m_abc])),f_c[0:m_abc]))
#sam_x = np.vstack((f_a[0:m_abc],f_b[0:m_abc]))
##sam_x = np.array(sam_x)

'''
#calculate the mean
tmp_mean = np.mean(sample_x,0)
#sample_x = sample_x - tmp_mean
for i in range(sample_x.shape[0]):
    for j in range(feature_no):
        if sample_x[i][j] != 0:
            sample_x[i][j] = sample_x[i][j] - tmp_mean[j]
'''

if str('4') in s:
    covar_m = np.cov(sample_x.T)
else:
    covar_m = np.matmul(sample_x.T,sample_x)


values,vectors = eigh(covar_m,)
eigen_sum = sum(values)

k = 1 
tmp_sum = 0
if str('4') in s:
    while(tmp_sum < 0.85 *eigen_sum):
        tmp_sum = tmp_sum + values[-k]
        k = k + 1
else:
    k = 11


eigh_v = vectors[:,feature_no-k:feature_no-1].T
feature_x = np.matmul(sample_x,eigh_v.T)
dump_svmlight_file(feature_x,data_y,filename_out)















