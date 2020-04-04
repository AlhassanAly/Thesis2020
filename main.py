import networkx as nx
from networkx.algorithms import node_connectivity
import matplotlib.pyplot as plt
import pylab
import math
import json   
import random 
import itertools

G = nx.Graph(name = "Cloud-Fog-Network")
G.add_node("C")

medium_speed = 299792458  # speed of light
fogs = 10
fog_range = 0.4
Edge_devices = 5 

positions ={}
attributes = {}
fog_list = []

for n in range (1,fogs+1):
    G.add_node("f" + str(n))

for n in range (1,Edge_devices+1):
    G.add_node("d" + str(n))

node_positions = {"C":(0,0.6)}
node_attrs = {"C":{"MIPS": 5000, "STR": 500000}}


def place_fogs(x1 = -0.7,x2 = 0.7 ,y1 = -0.3, y2 = 0.1, mips_low = 200, mips_high=900, 
str_low = 512, str_high = 2048):
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

def inRange_Clustering(candidate_list):

    cluster_list ={}  
    min_cluster = {}

    #new approach
    for fold in range(1, len(candidate_list)+1):
        for comb in itertools.combinations(candidate_list, fold):
            storage = 0
            for node in comb:
                storage += G.nodes[node]["STR"]
                if storage >= G.nodes[d]["Size"]:
                    cluster_list[comb] = storage
    if cluster_list != {}:
        minimum_comb = min(cluster_list, key = cluster_list.get)
        minimum_ST = cluster_list[minimum_comb]
        min_cluster[minimum_comb]=minimum_ST           
    return cluster_list, min_cluster


def getMaxStorage(candidate_list):
    max_storage = 0
    for node in candidate_list:
        max_storage += G.nodes[node]["STR"]   
    return max_storage

def fogNeighbour_Clustering(d, candidate_list):

    neighbour_list = []
    all_neighbours = {}
    neighbor_candidates = []
    max_storage = getMaxStorage(candidate_list)

    for fog in candidate_list:
        for global_fog in fog_list:
            if fog != global_fog:
                fog_position = fnode_pos[fog]
                global_fog_position = fnode_pos[global_fog]
                dist = calculateDistance(fog_position[0], fog_position[1], global_fog_position[0], global_fog_position[1])
                if dist < fog_range:
                    neighbour_list.append(global_fog)
                      
        all_neighbours[fog] = neighbour_list
    
    print ("all neighbours", all_neighbours)

    for fog, neighbour in all_neighbours.items():
       
        neighbor_candidates.append(fog)
        for n in neighbour:
            if (max_storage + G.nodes[n]["STR"]) >=  G.nodes[d]["Size"]:
                G.add_edges_from([(fog, n)])
                neighbor_candidates.append(n)
        
    return neighbor_candidates

       
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

candidate_list = []

for d in G.nodes:
    if 'd' in d:
        candidate_list = list(G.adj[d])
        if candidate_list != []:
            print("candidate list for", d, ":", candidate_list)
            response_times = {}
            found_fog = False
            for candidate in candidate_list:

                if G.nodes[candidate]["STR"] >= G.nodes[d]["Size"]:
                    found_fog = True
                    print(candidate +" STR:", G.nodes[candidate]["STR"], d + " Size:", G.nodes[d]["Size"], " Valid capacity")
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
                    print("response times for",d, ":", response_times) 
            
            if not found_fog:

                    cluster_list, min_cluster = inRange_Clustering(candidate_list)
                    #print ("function return", cluster_list, min_cluster)
                    print("cluster list for", d, ":" , cluster_list)
                    print ("minimum cluster", min_cluster)  

                    if cluster_list == {}:
                        new_candidate_list = fogNeighbour_Clustering(d, candidate_list)
                        cluster_list, min_cluster = inRange_Clustering(new_candidate_list)
                        print("cluster list for", d, ":" , cluster_list)
                        print(node_attrs)
                        print ("new minimum cluster", min_cluster)  


            if response_times != {}:
                minimum_RT = min(response_times, key = response_times.get)
                time = response_times[minimum_RT]
                print("Minimum response time for",d, ":", minimum_RT, time)
     




 

print("done")                    


nx.draw(G, pos = node_positions, nodelist = ["C"],
node_size = 2000, alpha = 0.3, node_color = "r", with_labels=True, font_size = 9)

nx.draw(G, pos = fnode_pos , nodelist = fog_list, 
node_size = 600, alpha = 0.2, node_color = "b", with_labels=True, font_size = 9)

nx.draw(G, pos = node_pos, nodelist = device_list,
node_size = 150, alpha = 0.5, node_color = "g", with_labels=True, font_size = 9)

plt.show()

