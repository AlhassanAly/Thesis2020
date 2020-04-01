import networkx as nx
import matplotlib.pyplot as plt


G = nx.Graph()
G.add_node("C")
G.add_edges_from([("C", "F1"), ("C", "F2"), ("C", "F3"),
("F1", "D1"), ("F1", "D2"), ("F1", "D3"),("F1", "D4"),
("F2", "D1"), ("F2", "D2"), ("F2", "D3"),("F2", "D4"),
("F3", "D1"), ("F3", "D2"), ("F3", "D3"),("F3", "D4")])
#MIPS = instructions/second 
#STR = MB
node_attrs = {"C":{"MIPS": 3000, "STR": 6500},
              "F1":{"MIPS": 200, "STR": 2000},
              "F2":{"MIPS": 700, "STR": 512},
              "F3":{"MIPS": 200, "STR": 1000},
              "D1":{"mINS": 500, "Size": 1800},
              "D2":{"mINS": 200, "Size": 900},
              "D3":{"mINS": 100, "Size": 400},
              "D4":{"mINS": 100, "Size": 400}}

#node attributes
nx.set_node_attributes(G, node_attrs)





# Link/edge attributes
# DR = Data rate 5G = (Down) 200 Mbit/s ,(Up) 100 Mbit/s - we use 150
 
# LT = latency 5G = avg 5ms (see notes)
edge_attrs = {("C","F1"): {"DR": 3000},
              ("C","F2"): {"DR": 3000},
              ("C","F3"): {"DR": 3000},
              ("F1","D1"):{"DR": 3000},
              ("F1","D2"):{"DR": 1000},
              ("F1","D3"):{"DR": 2000},
              ("F2","D1"):{"DR": 2500},
              ("F2","D2"):{"DR": 5000},
              ("F2","D3"):{"DR": 1650},
              ("F3","D1"):{"DR": 1500},
              ("F3","D2"):{"DR": 9000},
              ("F3","D3"):{"DR": 1600},
              ("F1","D4"):{"DR": 3000}}




nx.set_edge_attributes(G, edge_attrs)

print(nx.node_connectivity(G, "F1", "D4"))
"""

medium_speed = 299792458

propagation_delay = fog_device_distances / medium_speed

serialization_delay = app_size / data_rate

network_latency = propagation_delay + serialization_delay

processing_time = mINS/MIPS

response_time = processing_time + network_latency

"""
#print(nx.neighbors(G, 'C'))
print(nx.node_connected_component(G, "C"))
#print(nx.nodes(G))
#print(nx.edges(G))
"""
def check_capacity():

    for element in nx.nodes(G):
        if G.nodes[element].get("Size"):
            print(G.nodes[element].get("Size"))
        # print(G.nodes[element].get("STR"))
    
check_capacity()

"""
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
