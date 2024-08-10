#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib.pyplot as plt


# # Load Countries

# In[2]:


with open('source.txt') as file:
    lines = file.readlines()

names = list(map(lambda line: line.split('\t')[1], lines))
print(f"Total number of countries: {len(names)}")


# # Get start and end sets

# In[3]:


def getEndSets(words):
    starts = {}
    finishes = {}

    for name in words:
        s = name[0].lower()
        f = name[-1].lower()
        starts[s] = starts.get(s, []) + [name]
        finishes[f] = finishes.get(f, []) + [name]

    return starts, finishes

starts, finishes = getEndSets(names)


# # Build Networkx graph from countries and sets

# In[4]:


def buildGraph(countries):
    G = nx.DiGraph()
    starts, finsihes = getEndSets(countries)
    
    # Add nodes
    for name in countries:
        G.add_node(name)
    
    # Add edges
    for curr in names:
        f = curr[-1].lower()
        children = starts.get(f, [])
        for child in children:
            if child != curr:
                G.add_edge(curr, child)
    
    return G


# In[5]:


G = buildGraph(names)
print(G)


# In[10]:


sources = [node for node, deg in G.in_degree() if deg == 0]
sinks = [node for node, deg in G.out_degree() if deg == 0]
print(f"Total sources : {len(sources)}")
print(f"Total sinks   : {len(sinks)}")


# # Get grand-child set
# This could potentially be used for pruning.
# 
# Depths guide:
# 1. Children
# 2. Grand-children
# 3. Great-grand-children

# In[46]:


def family(graph, node, depth, familyset=None):
#     print(f"Getting familiy for: {node}")
    if depth == 0:
        return familyset
    
    if familyset == None:
        familyset = set([node])
    
    children = list(graph.successors(node))
    familyset.update(children)
    
    for child in children:
#         print(f"About to recurse to child: {child}")
        family(graph, child, depth-1, familyset=familyset)

    return familyset


# In[47]:


ggrand = family(G, 'Albania', 3)
print(ggrand)
print(f"Albania has {len(ggrand)} great-grand-children")


# In[48]:


grandChildSizes = {node: len(family(G, node, 3)) for node in names}
sortedNames = sorted(names, key=lambda n: grandChildSizes[n])
for name in sortedNames:
    print(grandChildSizes[name], name)


# # Use great-grand-child sets as heuristic
# Recursively try the first $n$ paths available as ranked by largest family size.

# In[54]:


def findLong(graph, famSizes, node, path=[], longest=[], N=3):
    children = list(graph.successors(node))
    children = list(filter(lambda c: c not in path, children))
    
    children = list(sorted(
        children,
        key=lambda n: famSizes[n],
        reverse=True
    ))[:N]
    print(f"From {node} pruned to these: {children}")
    for child in children:
        if child not in path:
            newpath = path + [child]
            if len(newpath) > len(longest):
                longest = newpath
            # print(f"Built path: {newpath}")
            print(f"Longest path: {len(longest)}")
            findLong(graph, famSizes, child, path=newpath, longest=longest, N=N)
    
    return longest


# In[55]:


l = []
longestPath = findLong(G, grandChildSizes, 'Albania', longest=l, N=3)
print(longestPath)
print(l)


# In[ ]:




