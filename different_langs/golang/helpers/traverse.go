package helpers

import (
	"fmt"
)

type Path struct {
	head		*Node
    tail		*Node
    visitCounts	map[string]int
    steps 		[]*Node
    graph		*Graph
}

func nodeArrToString(nodes []*Node) string {
	out := ""
	for _, n := range nodes {
		out += ", "
		out += n.unit
	}
	return out
}

/*
Gets the possible steps from the tail of the path.
If there are no steps, then will be an empty arr.
Accounts for max possible visits based on node size.
*/
func (p *Path) getNextSteps() []*Node {
	childNodes := p.graph.getChildren(p.tail)

	availableSteps := make([]*Node, 0)
	for _, n := range childNodes {
		if (p.visitCounts[n.unit] < n.size) {
			availableSteps = append(availableSteps, n)
		}
	}

	return availableSteps
}

func (p *Path) init(n *Node) {
	p.head = n
	p.tail = n
	p.visitCounts[n.unit] = 1
	p.steps = append(p.steps, n)
}

func (p *Path) visit(n *Node) {
	p.tail = n
	p.visitCounts[n.unit] += 1
	p.steps = append(p.steps, n)
}

func (p *Path) toString() string {
	out := ""
	for _, node := range p.steps {
		out += " -> "
		out += node.unit
	}
	return out
}

func (p *Path) expand() {
	for {
		children := p.getNextSteps()
		if len(children) == 0 {
			break
		}
		p.visit(children[0])
	}
}

func BuildPath(n *Node, g *Graph) Path {
	// counts := make(map[*Node]int)
	// counts[n] = 1
	counts := make(map[string]int)
	counts[n.unit] = 1
	steps := []*Node{n}

	return Path{n, n, counts, steps, g}
}

func Traverse(g *Graph) {
	var path Path

	// Construct path from random node
	for _, value := range g.nodes {
		path = BuildPath(&value, g)
		break
	}

	// // Start with specific node
	// // startNode := g.nodes["nr"]
	// startNode := g.nodes["an"]
	// fmt.Println("Got starting node", &startNode)
	// path = BuildPath(&startNode, g)

	path.expand()

	for key, value := range path.visitCounts {
		fmt.Println("  ", key, value, "/", g.nodes[key].size)
	}
	fmt.Println("Final path:", path.toString())


	/*
	Real logic should be this:
	1. For each node build a path object.
	2. || Expand paths out randomly
	3. Sort nodes by path depth
	4. Repeat steps 1..3 for N times
	5. Once there are no updates to topo sort order (or stable cycle)
		then stop.

	Now we have a *rough* topological sort,
	and can do a thorough cached-BFS traversal from bottom-up.


	TODO:
	- Cleanly get array from map keys/values?
	- Cleanly sorting array?
	*/
}




