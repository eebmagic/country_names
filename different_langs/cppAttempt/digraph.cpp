#include <iostream>
#include <vector>
#include <unordered_map>

typedef std::unordered_map<int, std::vector<int>> Graph;

// Insert a node to the map.
void addNode(Graph& graph, int id, const std::vector<int>& edges) {
    graph[id] = edges;
}

std::vector<int>& getNode(Graph& graph, int id) {
    
}

