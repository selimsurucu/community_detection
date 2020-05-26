# -*- coding: utf-8 -*-
"""
Created on Tue May 26 22:32:49 2020

@author: selim
"""


import networkx as nx
import sys
from cdlib import algorithms # detection algoritmaları için kütüphane
import os 
# INIT

parametres = sys.argv # parametreleri okuyup set ettik
nTop = sys.argv[2]# son parametre ntop olarak set edildi.
retweet_folder = sys.argv[1]
print(retweet_folder)
G = nx.DiGraph() 

# 

# RESULT OF COMMUNITY ALG.
def community_size(com):
    print("Community_size = " +str(len(com)))
    print("Max element_count = " + str(len(com[0])))
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

"""
# GET INFO OF COMMUNITIES 
def get_communities(com):
    for i in range(0,int(nTop)):
        print("community_size = "  + str(len(com[i])))
        print(com[i])
        print("xxxxxxxxxxxxxxxxx")
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
        
def writeComToFile (com):
    file = open('results/communities.txt','w') 
    for i in range(0,int(nTop)):   
        file.write( "community_"+str(i+1) +"=" + str(com[i]) +"\n")
    print("Path of Community Results = "+ os.path.realpath(file.name))
    file.close()
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


    
# Dosyaların okunduğu ve grafa edgelerin eklendiği kısım.
for entry in os.listdir(retweet_folder):
    print('reading retweet edges from file ('+entry+')...')
    if os.path.isfile(os.path.join(retweet_folder, entry)):
        fhand = open(os.path.join(retweet_folder, entry))
        for line in fhand:
            lst = line.strip().split(',')
            if len(lst[0])==0 or len(lst[1])==0:
                continue
            G.add_weighted_edges_from([(lst[0],lst[1],int(lst[2]))])
        
print("file reading complete!")
print("node count " + str(len(G.nodes())))
print("\n")

# LEIDEN ALGORITHMS
lei_com = algorithms.leiden(G)
community_size(lei_com.communities)
#get_communities(lei_com.communities)

# Check Results Folder
if os.path.isdir("results") == False:
    os.mkdir("results")
    print("Results Folder is created \n")

writeComToFile(lei_com.communities)
