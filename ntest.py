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

# Create nodes and add them to the graph
for name in names:
    G.add_node(name)

# Create dictionaries to store nodes starting with a specific letter and ending with a specific letter
starts = {}
finishes = {}

for name in names:
    s = name[0].lower()
    f = name[-1].lower()
    starts[s] = starts.get(s, []) + [name]
    finishes[f] = finishes.get(f, []) + [name]

# Create edges based on the starting and finishing letters
sinks = []
sources = set(names.copy())
edgeCount = 0
for i, curr in enumerate(names):
    f = curr[-1].lower()
    children = starts.get(f, [])
    if curr in children:
        children.remove(curr)

    # print(f"{i}) {curr} has {len(children)} children")
    if len(children) == 0:
        sinks.append(curr)

    for child in children:
        G.add_edge(curr, child)
        edgeCount += 1

        if child in sources:
            sources.remove(child)

print(f"Total number of edges: {edgeCount}")
print(f"\nSinks:")
print('\t' + '\n\t'.join(sinks))
print(f"Sources:")
print('\t' + '\n\t'.join(sorted(sources)))


def dfs(node, path):
    global longest
    print(len(longest), len(path), node)
    for neighbor in G.neighbors(node):
        if neighbor not in path:
            newpath = path + [neighbor]
            # print(f"New path: {newpath}")
            dfs(neighbor, newpath)

    if len(path) > len(longest):
        longest = path

longest = []
try:
    for start in G:
        print(f"Computing paths from {start} ...")
        dfs(start, [start])
        print(f"Curr longest: {len(longest)}")
except KeyboardInterrupt:
    print("STOPPING LOOP")

print(f"\nLONGEST PATH:")
print('\t' + '\n\t'.join(longest))


print(F"DRAWING GRAPH...")
nx.draw(G, pos=nx.circular_layout(G))
nx.draw_networkx_labels(G, pos=nx.circular_layout(G))
print(F"SHOWING GRAPH...")
plt.show()
