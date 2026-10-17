from dataclasses import dataclass, field
from typing import Dict, List, Set

@dataclass
class Graph:
    nodes: Set[str] = field(default_factory = set)
    edges: Dict[str, List[str]] = field(default_factory = dict)
    atributes: Dict[str, Dict] = field(default_factory = dict)
    
    def node_str(self, node: str):
        if type(node) is not str:
            return str(node)
        return node
    
    def add_node(self, node: str=None):
        if node is None:
            node = len(self.nodes)
        node = self.node_str(node)
        if node in self.nodes:      # obstoječega vozlišča ne ponastavimo (ohranimo povezave)
            return
        self.nodes.add(node)
        self.edges[node] = []
        self.atributes[node] = {}
    
    def add_edge(self, node1: str, node2: str):
        node1 = self.node_str(node1)
        node2 = self.node_str(node2)
        
        if node1 not in self.nodes:
            self.add_node(node1)
        if node2 not in self.nodes:
            self.add_node(node2)
        if node1 == node2 or node2 in self.edges[node1]:   # brez zank in večkratnih povezav
            return

        self.edges[node1].append(node2)
        self.edges[node2].append(node1)
    
    def remove_node(self, node: str):
        node = self.node_str(node)
        if node not in self.nodes:
            raise ValueError(f"Node [{node}] not in graph, and cannot be removed.")
        self.nodes.remove(node)
        del self.edges[node]
        del self.atributes[node]
        for n in self.nodes:
            if node in self.edges[n]:
                self.edges[n].remove(node)
    
    def remove_edge(self, node1: str, node2: str):
        node1 = self.node_str(node1)
        node2 = self.node_str(node2)
        if node1 not in self.nodes:
            raise ValueError(f"Node [{node1}] not in graph, and cannot remove edge.")
        
        if node2 not in self.nodes:
            raise ValueError(f"Node [{node2}] not in graph, and cannot remove edge.")
    
        if node2 not in self.edges[node1]:
            raise ValueError(f"Edge [{node1}] -> [{node2}] not in graph, and cannot be removed.")
        
        self.edges[node1].remove(node2)
        self.edges[node2].remove(node1)
        
    def edge_info(self):
        return self.edges
    
    def degree(self, node: str):
        return len(self.edges[self.node_str(node)])

    def number_of_edges(self):
        return sum(len(s) for s in self.edges.values()) // 2

    def __str__(self):
        return f"Graph with {len(self.nodes)} nodes and {self.number_of_edges()} edges."
    
    def __len__(self):
        return len(self.nodes)
    
    def __iter__(self):
        return iter(self.nodes)