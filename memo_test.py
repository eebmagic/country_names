import networkx as nx
import tempfile
import subprocess
import matplotlib.pyplot as plt

# Read the list of countries from source.txt
with open('source.txt') as file:
    lines = file.readlines()

# Create a directed graph using NetworkX
G = nx.DiGraph()

names = list(map(lambda line: line.split('\t')[1], lines))
print(f"Total number of countries: {len(names)}")

merges = {}
mergeable = set()
for name in names:
    s = name[0].lower()
    f = name[-1].lower()

    if s == f:
        merges[s] = merges.get(s, []) + [name]
        mergeable.add(name)
print(mergeable)

merged = []
for name in names:
    if name not in mergeable:
        merged.append(name)

for mset in merges.values():
    merged.append(', '.join(mset))
merged = sorted(merged)

print('\t' + '\n\t'.join(merged))

print(f"Total nodes before: {len(names)}")
print(f"Total nodes after: {len(merged)}")
