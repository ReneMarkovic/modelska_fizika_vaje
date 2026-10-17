from .graph_structure import Graph

def average_degree(G: Graph):
    return sum(len(G.edges[node]) for node in G.nodes) / len(G.nodes)

def graph_density(G: Graph):
    n = len(G.nodes)
    return 2 * G.number_of_edges() / (n * (n - 1))

def node_degree(G: Graph, node: str):
    return len(G.edges[node])

def local_clustering_coefficient(G: Graph, node: str):
    neighbors = G.edges[node]
    if len(neighbors) < 2:
        return 0
    n = 0
    for i in range(len(neighbors)):
        for j in range(i+1, len(neighbors)):
            if neighbors[j] in G.edges[neighbors[i]]:
                n += 1
    return n / (len(neighbors) * (len(neighbors) - 1) / 2)

def clustering_coefficient(G: Graph):
    return sum(local_clustering_coefficient(G, node) for node in G.nodes) / len(G.nodes)