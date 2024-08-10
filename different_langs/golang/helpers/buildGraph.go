package helpers

import (
    "fmt"
    // "reflect"
)

type Node struct {
    unit        string
    head        string
    tail        string
    size        int
    children    []string    // The actual country names that fall under this node
}

type Graph struct {
    // a map of unit strings to nodes
    nodes       map[string]Node
    // edges as a map of unit strings to child nodes
    edges       map[string]map[string]struct{}
}

func (g *Graph) getChildren(n *Node) []*Node {
    childrenSet := g.edges[n.unit]

    arr := make([]*Node, len(childrenSet))
    idx := 0
    for key, _ := range childrenSet {
        node := g.nodes[key]
        arr[idx] = &node
        idx += 1
    }


    return arr
}


func generateUnit(name string) string {
    start := string(name[0])
    end := string(name[len(name)-1])
    unit := start + end
    return unit
}

func (n *Node) addChild(name string) {
    n.children = append(n.children, name)
    n.size++
}

func (g *Graph) addEdge(from, to string) {
    // Check that both strings point to existing nodes
    _, fromExists := g.nodes[from]
    if !fromExists {
        fmt.Printf("Failed to add edge: %s => %s\n", from, to)
    }
    _, toExists := g.nodes[to]
    if !toExists {
        fmt.Printf("Failed to add edge: %s => %s\n", from, to)
    }

    // Update the array
    if g.edges[from] == nil {
        g.edges[from] = make(map[string]struct{})
    }
    g.edges[from][to] = struct{}{}
}


func BuildNode(name string) Node {
    start := string(name[0])
    end := string(name[len(name)-1])
    unit := start + end
    children := []string{name}

    return Node{unit, start, end, 1, children}
}

func BuildGraph(names []string) Graph {
    // Generate a map of start/end strings to Nodes
    nodes := make(map[string]Node)
    
    for _, name := range names {
        unit := generateUnit(name)
        existing, exists := nodes[unit]
        if exists {
            existing.addChild(name)
            nodes[unit] = existing
        } else {
            node := BuildNode(name)
            nodes[unit] = node
        }
    }

    // Build a graph structure
    edges := make(map[string]map[string]struct{})
    graph := Graph{nodes, edges}

    // Build the edges in the graph
    for unitA, nodeA := range nodes {
        for unitB, nodeB := range nodes {
            if nodeA.tail == nodeB.head {
                graph.addEdge(unitA, unitB)
            }
        }
    }

    return graph
}
