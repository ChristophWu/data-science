# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 23:10:28 2018

@author: Jason
"""

import networkx as nx
#import numpy as np
#import operator
import time
import sys


start = time.clock()

G = nx.Graph()
#G.add_node('A',name = 'a_node',weight=5)
#print(G.node['A'])
#if (G.has_node('A')):
#    G.remove_node('A')

# read all edges
sample_input = str(sys.argv[1])
sample_output = str(sys.argv[2])

#sample_input = 'sample_input1.txt'
#sample_output = 'sample_output.txt'
edges = open(sample_input,encoding = 'utf-8')
while True:
    line = edges.readline()
    if not line:
        break
    line = line.split(' ')
    G.add_edge(int(line[0]),int(line[1].strip()))
edges.close()

all_nodes = [i for i in G.nodes()]
#for i in all_nodes:
#    print(i)
#print(all_nodes)
#tmp = all_nodes
#for i in tmp:
#    print(i)
#    if(G.degree(i) < 5):
#        all_nodes.remove(i)
#print(all_nodes)
potential_clique = []
skip_nodes = []

maximum = 0 

def change_max(a):
    global maximum
    maximum = a

def write_csv(potential_clique):
    with open(sample_output,'w') as out:
        output = sorted(potential_clique)
        for i in output:
            out.write(str(i) + '\n')

def find_cliques(potential_clique=[], remaining_nodes=[], skip_nodes=[]):

    # To understand the flow better, uncomment this:
    # print (' ' * depth), 'potential_clique:', potential_clique, 'remaining_nodes:', remaining_nodes, 'skip_nodes:', skip_nodes
    time_use = time.clock() - start
    if (time_use > 177):
        if(len(potential_clique)>maximum):
            change_max(len(potential_clique))
            print('This is a clique:', potential_clique,'time',time_use)
            write_csv(potential_clique)
            return
#        print('This is a clique:', potential_clique,'time',time_use)
#        write_csv(potential_clique)
#        return
#    if (depth >=1200):
#        print('This is a clique:', potential_clique,'time',time_use)
#        write_csv(potential_clique)
#        return
    if (len(remaining_nodes) == 0) and (len(skip_nodes) == 0):
        if(len(potential_clique)>maximum):
            change_max(len(potential_clique))
            print('This is a clique:', potential_clique,'time',time_use)
            write_csv(potential_clique)
            return

    for node in remaining_nodes:

        # Try adding the node to the current potential_clique to see if we can make it work.
        new_potential_clique = potential_clique + [node]
        new_remaining_nodes = [n for n in remaining_nodes if n in list(G[node])]
        new_skip_list = [n for n in skip_nodes if n in list(G[node])]
        find_cliques(new_potential_clique, new_remaining_nodes, new_skip_list)

        # We're done considering this node.  If there was a way to form a clique with it, we
        # already discovered its maximal clique in the recursive call above.  So, go ahead
        # and remove it from the list of remaining nodes and add it to the skip list.
        remaining_nodes.remove(node)
        skip_nodes.append(node)

find_cliques(remaining_nodes=all_nodes)




























































