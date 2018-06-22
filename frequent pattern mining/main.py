# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 21:13:08 2018

@author: Jason
"""

from itertools import combinations
import sys
import multiprocessing as mp
from multiprocessing import Manager

class Fpnode(object):
    def __init__(self, value, count, parent):
        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []
        
    def get_child(self,value):
        for node in self.children:
            if node.value == value:
                return node
        return None
    
#    def add_child(self, value):
#        chlid = Fpnode(value,1,self)
#        self.children.append(child)
#        return child
def get_frequent_pattern(frequent_list,frequency):
    fre_list = frequent_list
    fre = frequency
    for m in range(0,len(fre_list)):
        for sub in combinations(fre_list[1:],m):
            sub = list(sub)
            sub.append(fre_list[0])
            for item in range(len(sub)):
                sub[item] = int(sub[item])
            sub.sort()
            pattern = tuple(sub)
            if pattern in frequent_pattern.keys():
                frequent_pattern[pattern] += fre
            else:
                frequent_pattern[pattern] = fre
    
#def job(x):
#    t = tmp_head[x]
#    tmp = header[t]
#    while tmp is not None:
#        fre_tmp = []
#        if(tmp.count >= 1):
#            tmp_par = tmp
#            fre_tmp.append(tmp_par.value)
#            while tmp_par.parent is not None:
#                tmp_par = tmp_par.parent
#                if(tmp_par.value != -1):
#                    fre_tmp.append(tmp_par.value)
#            get_frequent_pattern(fre_tmp,tmp.count)
#        # get frequent pattern use fre_tmp. e.g.(1,4,5,8) conditioned on 2
#        tmp = tmp.link


## read data ###
#input_file = 'sample2.in'
#output_file = 'output.txt'
#min_support = 0.1

input_file = sys.argv[2]
output_file = sys.argv[3]
min_support = float(sys.argv[1])

f = open(input_file, encoding = 'utf-8')
transaction = []
while(True):
    line = f.readline()
    if not line:
        break
    tmp = line[:-1].split(',')
    transaction.append(tmp)
f.close()

frequent_items_1 = {}
total_transaction = len(transaction)
min_threshhold = len(transaction) * min_support
trans = 5000
min_search = 1

if(total_transaction > trans):
    min_search = min_threshhold * 0.01
### get frequent_items_1 pattern ###
for item in transaction:
    for tmp in item:
        if tmp in frequent_items_1:
            frequent_items_1[tmp] += 1
        else:
            frequent_items_1[tmp] = 1
for key in list(frequent_items_1.keys()):
    if frequent_items_1[key] < min_threshhold:
        del frequent_items_1[key]

### get head table ###
header = {}
for key in frequent_items_1.keys():
    header[key] = None

### build fp-tree ###
root_value = -1
root = Fpnode(root_value, 0 ,None)
#aim_item = np.array(frequent_items_1.keys())
for item in transaction:
    ### get transaction and sort as frequency
    sort_item = []
    for i in item:
        if i in frequent_items_1:
            sort_item.append(i)
    sort_item.sort(key=lambda x:frequent_items_1[x], reverse = True)
    ### build sub-tree
    tmp_node =root
    for tmp in sort_item:
        child_ = tmp_node.get_child(tmp)
        if child_ is not None:
            child_.count += 1
        else:
            child_ = Fpnode(tmp, 1, tmp_node)
            tmp_node.children.append(child_)
            ### let the same commodity linked
            if header[tmp] == None:
                header[tmp] = child_
            else:
                c = header[tmp]
                while c.link is not None:
                    c = c.link
                c.link = child_
        tmp_node = child_

### get frequent pattern
#manager = Manager()
#frequent_pattern = manager.dict()
#tmp_head = list(header.keys())
#pool = mp.Pool(processes = 2)
#pool.map(job,range(len(tmp_head)))
        
frequent_pattern = {}
#for i in range(len(tmp_head)):
#    t = tmp_head[i]
#    print(t,header[t])

for i in header.keys():
    tmp = header[i]
    while tmp is not None:
        fre_tmp = []
        if(tmp.count >= min_search):
            tmp_par = tmp
            fre_tmp.append(tmp_par.value)
            while tmp_par.parent is not None:
                tmp_par = tmp_par.parent
                if(tmp_par.value != -1):
                    fre_tmp.append(tmp_par.value)
            re = get_frequent_pattern(fre_tmp,tmp.count)
        # get frequent pattern use fre_tmp. e.g.(1,4,5,8) conditioned on 2
        tmp = tmp.link

for key in list(frequent_pattern.keys()):
    if frequent_pattern[key] < min_threshhold:
        del frequent_pattern[key]

frequent_pattern = sorted(frequent_pattern.items(), key = lambda item:(len(item[0]),item[0]))
#s = str(frequent_pattern[12][0])[1:-1]
f1 = open(output_file, 'w', encoding = 'utf-8')
for item in frequent_pattern:
    s = str(item[0])[1:-1]
    s = s.replace(' ', '')
    if(s[-1] == ','):
        s = s[0:-1]
    ratio = item[1]/total_transaction
    ratio_ = ('%.4f' % ratio)
    s_tmp = s + ':' + str(ratio_) + '\n'
    #print(s_tmp)
    f1.write(s_tmp)
f1.close()

## out put tree ###
#tmp_r = []
#tmp_r.append(root) 
#k = 0
#for w in range(10):
#    tmp = []
#    if(tmp_r == None):
#        break
#    print('it is layer' + str(k))
#    k += 1
#    for i in tmp_r:
#        print('parent is' + str(i.value))
#        for j in i.children:
#            if j != None:
#                print(j.value,j.count)
#                tmp.append(j)
#    tmp_r = tmp









    