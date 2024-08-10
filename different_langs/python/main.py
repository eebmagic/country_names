import matplotlib.pyplot as plt

with open('source.txt') as file:
    lines = file.readlines()

names = [l.split('\t')[1].lower() for l in lines]
print(names)

counts = {}
mappings = {}
for name in names:
    start, stop = name[0], name[-1]
    x = start + stop
    counts[x] = counts.get(x, 0) + 1
    mappings[x] = mappings.get(x, []) + [name]

for key, value in counts.items():
    print(key, value)
    print(f'\t{mappings[key]}')


# Build graph
import networkx as nx
dg = nx.DiGraph()

# Add nodes
for key, count in counts.items():
    dg.add_node(key, count=count)

print(list(dg.nodes(data=True)))

# Add edges
for key in counts.keys():
    neighbors = filter(lambda x: x.startswith(key[-1]), counts.keys())
    dg.add_edges_from([(key, n) for n in neighbors])

print(list(dg.edges()))
print(len(dg.nodes()))
print(len(dg.edges()))


# Get strongly connected components
strong = list(nx.strongly_connected_components(dg))
sources = [s for s in strong if len(s) == 1]
# The sources will be collections of nodes that cant be reached from any other node

print(f"Found {len(sources)} sources")

# pos = nx.nx_agraph.graphviz_layout(dg, prog='dot')

# plt.figure(figsize=(10, 10))
# nx.draw(dg, pos, with_labels=True, node_size=3000, node_color='lightblue')
# plt.show()


for node in dg.nodes():
    countries = mappings[node]
    print(node, countries)

    c = '\n'.join(countries)
    tag = '#countriesDAG'
    edges = []
    for edge in dg.edges(node):
        edges.append(f'[[{edge[1]}]]')
    edgesString = '\n'.join(edges)

    fullString = f'''{tag}
# {node}

## Countries
{c}

## Edges
{edgesString}
'''

    title = f'mds/{node}.md'
    with open(title, 'w') as file:
        file.write(fullString)

    # print('=' * 80)
    # print(title)
    # print('-' * 80)
    # print(fullString)


print(f"finished writing file!!!")