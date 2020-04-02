import networkx as nx
from networkx.algorithms import node_connectivity
import matplotlib.pyplot as plt
import pylab
import math
import json   
import random 


G = nx.Graph(name = "Cloud-Fog-Network")
G.add_node("C")

medium_speed = 299792458  # speed of light
fogs = 3
fog_range = 0.4
Edge_devices = 5 


for n in range (1,fogs+1):
    G.add_node("f" + str(n))

for n in range (1,Edge_devices+1):
    G.add_node("d" + str(n))

node_positions = {"C":(0,0.6)}
node_attrs = {"C":{"MIPS": 5000, "STR": 500000}}


def place_fogs(x1 = -0.7,x2 = 0.7 ,y1 = -0.3, y2 = 0.1, mips_low = 200, mips_high=900, 
str_low = 512, str_high = 2048):
    positions ={}
    attributes = {}
    fog_list = []
    for number in range (1,fogs+1):
        positions = {"f" + str(number):(random.uniform(x1,x2),random.uniform(y1, y2))}
        attributes = {"f" + str(number):{"MIPS":random.randint(mips_low,mips_high),"STR":random.randint(str_low, str_high)}}
        fog_list.append("f" + str(number))
        node_positions.update(positions)
        node_attrs.update(attributes)
    for fog in fog_list:
        G.add_edges_from([("C", fog)])

    return node_positions, fog_list, attributes

fnode_pos, fog_list, attributes = place_fogs()



def place_devices(x1=-0.8, x2=0.8, y1=-0.6, y2=0.1, ins_low= 50, ins_high=2000 , size_low= 64, size_high=4096):
    positions ={}
    attributes = {}
    device_list = []
    for number in range (1,Edge_devices+1):
        positions = {"d" + str(number):(random.uniform(x1,x2),random.uniform(y1, y2))}
        attributes = {"d" + str(number):{"mINS":random.randint(ins_low,ins_high),"Size":random.randint(size_low, size_high)}}
        device_list.append("d" + str(number))
        node_positions.update(positions)
        node_attrs.update(attributes)
    return node_positions, device_list, attributes

node_pos, device_list, attributes = place_devices()

nx.set_node_attributes(G, node_attrs)


def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist


fog_coords = []
device_coords = []

for key, value in node_positions.items():
    if 'f' in key:
        myObj = {
            "id":key,
            "coordX":value[0],
            "coordY":value[1]
            }
        fog_coords.append(myObj)
    if 'd' in key:
        myObj = {
            "id":key,
            "coordX":value[0],
            "coordY":value[1]
            }
        device_coords.append(myObj)

        
fog_device_distances = []

for fog_dicts in fog_coords:
    for dev_dicts in device_coords:
        value = fog_dicts["id"], dev_dicts["id"], calculateDistance(fog_dicts["coordX"], fog_dicts["coordY"], dev_dicts["coordX"], dev_dicts["coordY"])
        fog_device_distances.append(value)


for elements in fog_device_distances:
    if(elements[2] < fog_range):
        G.add_edges_from([(elements[0], elements[1])])



link_attrs = {}        
def  add_link_attributes(data_rate_low = 1000, data_rate_high = 10000):
    for link in list(G.edges):
        link_attrs.update({link: {"DR": random.randint(data_rate_low, data_rate_high)}})
    return link_attrs

add_link_attributes()
nx.set_edge_attributes(G, link_attrs) 


#print(G.edges['C','f1'])
#print(nx.info(G))
#print(G.nodes)
print(G.edges)
canlist = []
for d in G.nodes:
    if 'd' in d:
        candlist = list(G.adj[d])
        if candlist != None:
            response_times = {}
            for candidate in candlist:
                print(d, candidate, G.nodes[candidate]["STR"], G.nodes[d]["Size"])
                if G.nodes[candidate]["STR"] >= G.nodes[d]["Size"]:
                    link_attributes = G.edges[str(candidate), str(d)]
                    DR = link_attributes['DR']
                    ser_delay = G.nodes[d]["Size"]/DR
                    for dis in fog_device_distances:
                        if candidate == dis[0] and d == dis[1]:
                            f_e_distance = dis[2]
                            prop_delay = f_e_distance/ medium_speed
                            network_latency = prop_delay + ser_delay
                    processing_time = G.nodes[d]["mINS"] / G.nodes[candidate]["MIPS"]
                    r_t = processing_time + network_latency
                    response_times[candidate] = r_t 
                #else:        
            print(response_times)
            if response_times != {}:
                minimum_RT = min(response_times, key = response_times.get)
                time = response_times[minimum_RT]
                print(time, minimum_RT)
            


                      
print("done")                    
# for n in G.edges:
#     if "d" in n[1]:
#       for keys, values in node_attrs.items():
#           if n[0] in keys:
#               print("STR: ",values["STR"])
        
#           if n[1] in keys:
#               print("SIZE:", values["Size"])
           

"""
fog_shit = (list(G.adj['d1']))
print(G.nodes[fog_shit[0]])
#print(nx.node_connected_component(G, "C"))

for n in G.nodes:
print(G.adj["d1"])
"""

#print(node_attrs["f1"])
#print(device_fog_connections)
#print(G.nodes["C"])

       
#print(nx.get_node_attributes(G,"Size"))
#print(nx.get_node_attributes(G,"STR"))
#print(link_attrs)
#print(nx.edges(G))
#print("list of nodes: ",list(G.nodes))
#print("list of links: ",list(G.edges))
#print("Connected nodes: ",list(nx.connected_components(G)))
#print("sorted Degress: ",sorted(d for n, d in G.degree()))
#print("clusters: ",nx.clustering(G))
#print("shortest path from node 3 to connected nodes: ", sp[3])



nx.draw(G, pos = node_positions, nodelist = ["C"],
node_size = 2000, alpha = 0.3, node_color = "r", with_labels=True, font_size = 9)

nx.draw(G, pos = fnode_pos , nodelist = fog_list, 
node_size = 600, alpha = 0.2, node_color = "b", with_labels=True, font_size = 9)

nx.draw(G, pos = node_pos, nodelist = device_list,
node_size = 150, alpha = 0.5, node_color = "g", with_labels=True, font_size = 9)

plt.show()

