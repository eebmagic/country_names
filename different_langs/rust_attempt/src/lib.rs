extern crate petgraph;
use petgraph::graph::{DiGraph, NodeIndex};
// use crate::petgraph::visit::Walker;
use std::collections::HashMap;

use pyo3::prelude::*;
// use pyo3::wrap_pyfunction;

#[pyclass]
struct GraphManager {
    graph: DiGraph<i32, i32>,
    node_map: HashMap<i32, NodeIndex>,
}

#[pymethods]
impl GraphManager {
    #[new]
    fn new() -> Self {
        GraphManager {
            graph: DiGraph::new(),
            node_map: HashMap::new(),
        }
    }

    fn add_node(&mut self, label: i32) {
        let node_index = self.graph.add_node(label);
        self.node_map.insert(label, node_index);
    }

    fn add_edges(&mut self, from_id: i32, edges: Vec<i32>) {
        if let Some(&source_node) = self.node_map.get(&from_id) {
            for to_id in edges {
                if let Some(&target_node) = self.node_map.get(&to_id) {
                    self.graph.add_edge(source_node, target_node, 1);
                } else {
                    eprintln!("Target node with id does not exist: {}", to_id);
                }
            }
        } else {
            eprintln!("Source node with id does not exist: {}", from_id);
        }
    }
}

#[pymodule]
fn rust_graph(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<GraphManager>()?;
    Ok(())
}

