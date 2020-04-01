import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_edge('A','B',weight=4) # specify edge data
G.add_edge('A','C',weight=8) # specify edge data
G.add_edge('B','C',weight=5) # specify edge data
G.add_edge('B','D',weight=4.5) # specify edge data
G.add_node('A', population=5)
G.add_node('B', population=15)
G.add_node('C', population=65)
G.add_node('D', population=0)
G.add_node('E', population=888)

val_map = {'A': 1.0,
'D': 0.5714285714285714,
'H': 0.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
red_edges = []

edge_colours = ['black' if not edge in red_edges else 'red'
for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'),
node_color = values, node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
nx.draw_networkx_edges(G, pos, weight=True)
plt.show()