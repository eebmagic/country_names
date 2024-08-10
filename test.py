import pydot
import tempfile
import subprocess

'''
Country list coming from here:
https://www.worldometers.info/geography/alphabetical-list-of-countries/
'''
with open('source.txt') as file:
    lines = file.readlines()

graph = pydot.Dot(graph_type='digraph')

names = list(map(lambda line: line.split('\t')[1], lines))
# print(list(names))

nodeMap = {}
starts = {}
finishes = {}
for name in names:
    # Add node to graph
    node = pydot.Node(name)
    nodeMap[name] = node
    graph.add_node(node)

    # Add node to sets for edges later
    s = name[0].lower()
    f = name[-1].lower()
    starts[s] = starts.get(s, []) + [node]
    finishes[f] = finishes.get(f, []) + [node]



edgeSet = set()
counts = {}
for name in names:
    print(f"Making edges for: {name}")
    currNode = nodeMap[name]
    f = name[-1].lower()
    children = starts[f]

    counts[currNode] = {
        "children": len(children),
        "parents": 0 if currNode not in counts else currNode[counts]['parents']
    }

    for child in children:
        edge = pydot.Edge(currNode, child)
        edgeSet.add(edge)
        graph.add_edge(edge)
        print(f"Added edge: {currNode}, {child}")

        # childCounts = counts.get(currNode)

print(f"FINSHED BUILDING")
print(f"Total num of nodes: {len(nodeMap)}")
print(f"Total num of edges: {len(edgeSet)}")
graph.set_prog('dot')
with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tempFile:
    print(f"Creating graph pdf...")
    tempFile.write(graph.create_pdf())
    print(f"Opening file... : {tempFile.name}")
    subprocess.run(['open', tempFile.name])
