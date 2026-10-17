import GraphAL as gal
from GraphAL import graph_metrics as gm
G = gal.Graph()

[G.add_node(i) for i in range(10)]

G.add_edge("0", "1")
G.add_edge("0", "2")
G.add_edge("0", "3")
G.add_edge("0", "4")
kavg =  gm.average_degree(G)
print(kavg)

G = gal.graph_generators.Morita(0.1,100,5)
print(G)