# -*- coding: utf-8 -*-
import os
import pickle
import matplotlib.pyplot as plt

os.chdir("E:\\5. Innovation")
papers = pickle.load( open( "papers.p", "rb" ) )

# Generating a set of Unique Authors by First authors signatures
authors = []
for paper in papers:
    authors.append(paper['signature'])
authors = list(set(authors))

# Generating blocks of papers that have authors or co-authors with the same signatures
blocks = {}
for author in authors:
    blocks[author] =  []

for i in range(1000):
    blocks[papers[i]['signature']].append(papers[i])
    #for coauthor in paper['coauth']:
    #    if coauthor in blocks.keys():
    #       blocks[coauthor].append(paper)

size = []
for key in blocks.keys():
    size.append(len(blocks[key]))

plt.scatter(range(max(size)), size)
plt.show()
        
pickle.dump( blocks, open( "blocks_firstOnly.p", "wb" ) )            

                                   
'''
1. Generate a list for each signature
2. 
'''