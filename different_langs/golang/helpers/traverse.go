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
*/
func (p *Path) getNextSteps() []*Node {
	// get children from graph for tail node
	// filter children to only include where visits wouldn't
	// result in the path exceeding the visit limit for the node 
	fmt.Println("Getting next steps on path from curr: ", p.head.unit)
	childNodes := p.graph.getChildren(p.tail)
	// fmt.Println("Got childrenUnits", childNodes)
	fmt.Println("Got childrenUnits", nodeArrToString(childNodes))

	// for child := range childNodes {

	// }

	availableSteps := make([]*Node, 0)
	for _, n := range childNodes {
		if (p.visitCounts[n.unit] < n.size) {
			availableSteps = append(availableSteps, n)
		}
	}
	// fmt.Println("available child nodes: ", availableSteps)
	fmt.Println("available child nodes:", nodeArrToString(availableSteps))

	return availableSteps
}

func (p *Path) init(n *Node) {
	p.head = n
	p.tail = n
	p.visitCounts[n.unit] = 1
	p.steps = append(p.steps, n)
}

func (p *Path) visit(n *Node) {
	fmt.Println("Visiting node: ", n.unit, "which has a size of", n.size)
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

func BuildPath(n *Node, g *Graph) Path {
	// counts := make(map[*Node]int)
	// counts[n] = 1
	counts := make(map[string]int)
	counts[n.unit] = 1
	steps := []*Node{n}
	fmt.Println("Building steps array with node:", n)

	return Path{n, n, counts, steps, g}
}

func Traverse(g *Graph) {
	// counts := make(map[*Node]int)
	// path := Path{nil, nil, counts, nil, g}
	// fmt.Println("Built this init path:", path)
	// fmt.Println("Path has this graph: ", path.graph.nodes)

	// startKey := range(g.nodes).First()
	// key, value := g.nodes.Map()
	// fmt.Println("Graph has these nodes:", key, value)
	fmt.Println("STARTING LOOP:\n");

	var path Path
	// for _, value := range g.nodes {
	// 	path = BuildPath(&value, g)
	// 	break
	// }
	startNode := g.nodes["aa"]
	fmt.Println("Got starting node", &startNode)
	// path = BuildPath(*g.nodes["aa"], g)
	path = BuildPath(&startNode, g)
	fmt.Println("Built this path:", path)


	i := 0
	// for i < 10 {
	for {
		children := path.getNextSteps()
		if len(children) == 0 {
			break
		}
		path.visit(children[0])
		fmt.Println("Path after visit", path.toString())
		fmt.Println("visit counts", path.visitCounts)
		for key, value := range path.visitCounts {
			fmt.Println("  ", key, value)
		}
		i++
	}
	fmt.Println("Final path:", path.toString())
}



















