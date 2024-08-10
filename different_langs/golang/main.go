package main

import (
    "fmt"
    "log"
    "strings"
    "countries/helpers"
)

func main() {
    records, err := helpers.ParseTSV("source.txt")
    if err != nil {
        log.Fatalf("Error parsing TSV file: %v", err)
    }

    // Parse the tsv file
    names := make([]string, 0)
    for idx, record := range records {
        if idx <= 1 {
            continue
        }
        name := strings.ToLower(record[1])
        // fmt.Println(name)
        names = append(names, name)
    }
    // fmt.Println(names)

    // Build the graph
    graph := helpers.BuildGraph(names)
    fmt.Println("")
    // fmt.Println("\nCreated this graph:\n")
    // fmt.Println(graph)

    helpers.Traverse(&graph)

    /*
    TODO: Add another helper file with custom traversal logic.
       This should respect the size attribute on nodes.
       Also should be parallelization friendly.

       Maybe should do something to cache the longest found path for a node.
       This would mean doing some sort of topological sort even tho it isn't a DAG
        (impossible to compute levels when cycles are preset).
    */
}
