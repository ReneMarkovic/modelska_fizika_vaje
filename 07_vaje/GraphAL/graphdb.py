from dataclasses import dataclass

@dataclass
class GraphAL:
    nodes: list
    nnodes_features: dict
    edges: list
    edge_features: dict