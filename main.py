import networkx as nx
from networkx.algorithms import node_connectivity
from binpacking import linear_programming_solver as LPS
from heuristics import first_fit_algorithm as FFA
import matplotlib.pyplot as plt
import math  
import random 
import itertools
import time
from Parameters import iterations, final_runtime, medium_speed, fogs, Edge_devices, use_heuristics
from output import storeResults
from Iterations import getAverage, getFileAverage
import statistics

#functions

def place_fogs(x1 = -0.5 ,x2 = 0.5 ,y1 = -3, y2 = -2, mips_low = 200, mips_high=900, 
ram_low = 512, ram_high = 4096, range_low = 500, range_high = 2500):
    for number in range (1,fogs+1):
        positions = {"f" + str(number):(random.uniform(x1,x2),random.uniform(y1, y2))}
        attributes = {"f" + str(number):{"MIPS":random.randint(mips_low,mips_high),"RAM":random.randint(ram_low, ram_high),"Range":random.randint(range_low, range_high)}}
        fog_list.append("f" + str(number))
        node_positions.update(positions)
        node_attrs.update(attributes)
    for fog in fog_list:
        G.add_edges_from([("C", fog)])

    return node_positions, fog_list, attributes

def place_devices(x1=-0.5, x2=0.5, y1=-3.2, y2=-2.3,tasks_low = 1, tasks_high = 100, tsize_low = 32, tsize_high = 256, tmINS_low = 1, tmINS_high  = 5):
    positions ={}
    attributes = {}
    device_list = []
    for number in range (1,Edge_devices+1):
        positions = {"d" + str(number):(random.uniform(x1,x2),random.uniform(y1, y2))}
        attributes = {"d" + str(number):{"Tasks":random.randint(tasks_low, tasks_high),
        "Tsize":random.randint(tsize_low, tsize_high),
        "TmINS":random.randint(tmINS_low, tmINS_high)}}
        device_list.append("d" + str(number))
        node_positions.update(positions)
        node_attrs.update(attributes)

    return node_positions, device_list, attributes


def Calculate_Response_Time(d, candidate1, candidate2, fog_device_distances, task_number, task_size,task_mINS):
    
    if candidate2 == None:
        link_attributes = G.edges[str(candidate1), str(d)]
        DR = link_attributes['DR']
        ser_delay = (task_number * task_size)/DR
        for dis in fog_device_distances:
            if candidate1 == dis[0] and d == dis[1]:
                f_e_distance = dis[2]
                prop_delay = f_e_distance * 2/ medium_speed
                network_latency = prop_delay + ser_delay
        processing_time = (task_number * task_mINS) / G.nodes[candidate1]["MIPS"]
        r_t = processing_time + network_latency
        #response_times[candidate] = r_t
        return r_t
    else:
        f2f_link_attributes = G.edges[str(candidate1), str(candidate2)]
        f2d_link_attributes = G.edges[str(d), str(candidate1)]

        DR_f2f = f2f_link_attributes['DR']
        DR_f2d = f2d_link_attributes['DR']

        ser_delay = (task_number * task_size)/(DR_f2f + DR_f2d)
        fog_position = fnode_pos[candidate1]
        global_fog_position = fnode_pos[candidate2]
        device_position = node_pos[d]
        
        f_f_distance = calculateDistance(fog_position[0], fog_position[1], global_fog_position[0], global_fog_position[1])  
        f_d_distance = calculateDistance(device_position[0], device_position[1], fog_position[0], fog_position[1])
        
        prop_delay_f2f = f_f_distance * 2/ medium_speed
        prop_delay_f2d = f_d_distance * 2/ medium_speed
        prop_delay = prop_delay_f2f + prop_delay_f2d
        network_latency = prop_delay + ser_delay
        processing_time = (task_number * task_mINS) / G.nodes[candidate2]["MIPS"]
        r_t = processing_time + network_latency
        return r_t


def inRange_Clustering(candidate_list, use_heuristics = False):

    cluster_list ={}  
    min_cluster = {}
    task_list = []
    fogs_ram = []
    cost = []
    fog_names = []
    for t in range(G.nodes[d]["Tasks"]):
       task_list.append((str(t), task_size)) 
    task_count = len(task_list)   
    #new approach
    for fold in range(1, len(candidate_list)+1):
        for comb in itertools.combinations(candidate_list, fold):
            storage = 0
            for node in comb:
                storage += G.nodes[node]["RAM"]
                if storage >= (G.nodes[d]["Tasks"] * task_size):
                    cluster_list[comb] = storage
    if cluster_list != {}:
        minimum_comb = min(cluster_list, key = cluster_list.get)
        minimum_ST = cluster_list[minimum_comb]
        min_cluster[minimum_comb]=minimum_ST
        for t in min_cluster.keys():
            for a in t:
                fogs_ram.append(G.nodes[a]["RAM"]) 
                cost.append(task_mINS/G.nodes[a]["MIPS"])
                fog_names.append(a)

    if not use_heuristics:
        task_assignment = LPS(task_list, task_count, fog_names,fogs_ram, cost)
    else:
        fog_info = list(zip(fog_names,fogs_ram))
        task_assignment =  FFA(task_list, fog_info, True)   
    return cluster_list, min_cluster, task_assignment


def getMaxStorage(candidate_list):
    max_storage = 0
    for node in candidate_list:
        max_storage += G.nodes[node]["RAM"]   
    return max_storage


def fogNeighbour_Clustering(d, candidate_list):

    neighbour_list = []
    all_neighbours = {}
    neighbor_candidates = []
    max_storage = getMaxStorage(candidate_list)

    for fog in candidate_list:
        neighbour_list = []
        for global_fog in fog_list:
            if fog != global_fog:
                fog_position = fnode_pos[fog]
                global_fog_position = fnode_pos[global_fog]
                dist = calculateDistance(fog_position[0], fog_position[1], global_fog_position[0], global_fog_position[1])
                if dist < G.nodes[fog]["Range"]:
                    neighbour_list.append(global_fog)
                      
        all_neighbours[fog] = neighbour_list
    
    print ("all neighbours", all_neighbours)

    for fog, neighbour in all_neighbours.items():
       
        neighbor_candidates.append(fog)
        for n in neighbour:
            if (max_storage + G.nodes[n]["RAM"]) >=  (G.nodes[d]["Tasks"] * task_size):
                G.add_edges_from([(fog, n)])
                neighbor_candidates.append(n)              

    neighbor_candidates = list(dict.fromkeys(neighbor_candidates))

    print ("neighbour candidates", neighbor_candidates)
        
    return neighbor_candidates, all_neighbours


def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 3779.5275591 
     return dist


def  add_link_attributes(cloud_datarate_low = 100, cloud_datarate_high = 1000, f2d_data_rate_low = 1000, f2d_data_rate_high = 10000):
    link_attrs = {}
    for link in list(G.edges):
        
        if 'C' in link[0]:
            link_attrs.update({link: {"DR": random.randint(cloud_datarate_low, cloud_datarate_high)}})
        else:
            link_attrs.update({link: {"DR": random.randint(f2d_data_rate_low, f2d_data_rate_high)}})
    return link_attrs


def plotGraph():
   nx.draw(G, pos = node_positions, nodelist = ["C"],
   node_size = 2000, alpha = 0.3, node_color = "r", with_labels=True, font_size = 9, width =0.2)

   nx.draw(G, pos = fnode_pos , nodelist = fog_list, 
   node_size = 600, alpha = 0.2, node_color = "b", with_labels=True, font_size = 9, width = 0.2)

   nx.draw(G, pos = node_pos, nodelist = device_list,
   node_size = 200, alpha = 0.3, node_color = "g", with_labels=True, font_size = 7, width = 0.2)
   plt.show()
   



instance_avg_fogs_inrange_cluster = []
instance_avg_fogs_neighbor_cluster = []


for i in range(0, iterations): 
    starttime = time.time()
    G = nx.Graph(name = "Cloud-Fog-Network")
    G.add_node("C")

    
    

    if use_heuristics:
        optimizer = "First Fit heuristic"
        filename = "FFA" 
    else:
        optimizer = "Integer Linear Programming"    
        filename = "ILP"

    suffix = str(fogs) + "fogs-" + str(Edge_devices) + "devices-" + str(filename) + '_' + str(i)
    positions ={}
    attributes = {}
    fog_list = []


    for n in range (1,fogs+1):
        G.add_node("f" + str(n))

    for n in range (1,Edge_devices+1):
        G.add_node("d" + str(n))

    node_positions = {"C":(0,1)}
    node_attrs = {"C":{"MIPS": 2000, "RAM": 64000}}




    fnode_pos, fog_list, attributes = place_fogs()




        
    node_pos, device_list, attributes = place_devices()


    nx.set_node_attributes(G, node_attrs)





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
        if(elements[2] < G.nodes[elements[0]]['Range']):
            G.add_edges_from([(elements[0], elements[1])])



            


    link_attrs = add_link_attributes()
    nx.set_edge_attributes(G, link_attrs)

    candidate_list = []




    devices_list = []
    resp_times_list = []
    methods_list = []
    inrange_cluster_num_fogs = []
    neighbor_cluster_num_fogs = []

    for d in G.nodes:

        if 'd' in d:
            devices_list.append(d)
            task_size = G.nodes[d]["Tsize"]
            task_mINS = G.nodes[d]["TmINS"]
            candidate_list = list(G.adj[d])
            if candidate_list != []:
                print("candidate list for", d, ":", candidate_list)
                response_times = {}
                response_times_cl1 = {}
                response_times_cl2 = {}
                found_fog = False
                send_to_cloud = False
                for candidate in candidate_list:

                    
                    if G.nodes[candidate]["RAM"] >= (G.nodes[d]["Tasks"] * task_size):
                        r_t = Calculate_Response_Time(d, candidate,None, fog_device_distances,G.nodes[d]["Tasks"], task_size,task_mINS)
                        response_times[candidate] = r_t
                        
                        found_fog = True

                if response_times != {}:
                    minimum_RT = min(response_times, key = response_times.get)
                    re_time = response_times[minimum_RT]
                    print("Minimum response time for",d, ":", minimum_RT, re_time)
                    resp_times_list.append(re_time)
                    methods_list.append("single fog")
                
                if not found_fog:

                        cluster_list, min_cluster, task_assignment = inRange_Clustering(candidate_list,use_heuristics = use_heuristics)
                        
                        if min_cluster != {}:
                            print ("minimum inrange cluster for", d, ':', min_cluster)
    
                            inrange_cluster_num_fogs.append(sum(len(f) for f in min_cluster.keys()))

                        for elem in task_assignment:
                            print(elem[0], "tasks in", elem[1]) 
                            r_t_c = Calculate_Response_Time(d, elem[1], None, fog_device_distances,elem[0], task_size,task_mINS)
                            response_times_cl1[elem[1]] = r_t_c
                            

                        if  response_times_cl1 != {}:   
                            total_rt = max(response_times_cl1, key = response_times_cl1.get)
                            total_time = response_times_cl1[total_rt] 
                            print("Total inrange cluster response time for",d, ":", total_rt, total_time)
                            resp_times_list.append(total_time)
                            methods_list.append("Inrange cluster")
                        

                        if cluster_list == {}:
                            
                            new_candidate_list, all_neighbours = fogNeighbour_Clustering(d, candidate_list)
                            cluster_list, min_cluster, task_assignment = inRange_Clustering(new_candidate_list, use_heuristics = use_heuristics)
                            if min_cluster != {}:
                                print ("minimum cluster with neighbors for", d, ":", min_cluster)

                                neighbor_cluster_num_fogs.append(sum(len(f) for f in min_cluster.keys()))

                            for elem in task_assignment:
                                print("neighbor assignment:",elem[0], "tasks in", elem[1])
                                if elem[1] in candidate_list:
                                    r_t_cl2 = Calculate_Response_Time(d, elem[1], None, fog_device_distances,elem[0], task_size,task_mINS)
                                    response_times_cl2[elem[1]] = r_t_cl2
                                else:
                                    for fog, neighbours in all_neighbours.items():
                                        if elem[1] in neighbours:
                                            O_G = fog
                                            link_attrs = add_link_attributes()
                                            nx.set_edge_attributes(G, link_attrs)
                                            r_t_cl2 = Calculate_Response_Time(d, O_G, elem[1], fog_device_distances, elem[0], task_size, task_mINS)
                                            response_times_cl2[elem[1]] = r_t_cl2

                        if  response_times_cl2 != {}:  
                            total_rtn = max(response_times_cl2, key = response_times_cl2.get)
                            total_time_n = response_times_cl2[total_rtn] 
                            print("Total neighbor cluster response time for",d, ":", total_rtn, total_time_n)
                            resp_times_list.append(total_time_n)
                            methods_list.append("Neighbor cluuster")
                        else: 
                            send_to_cloud = True 

                if send_to_cloud == True:
                
                    f2d_distances = {}
                    for candidate in candidate_list:
                        fog_position = fnode_pos[candidate]
                        device_position = node_pos[d]
                        calc_dits = calculateDistance(fog_position[0], fog_position[1], device_position[0], device_position[1])
                        f2d_distances[candidate] = calc_dits
                    closest_candidate = min(f2d_distances, key = f2d_distances.get)       
                    print("App in", d, "is sent to Cloud through", closest_candidate)   
                    cloud_response_time = Calculate_Response_Time(d,closest_candidate,'C', fog_device_distances, G.nodes[d]["Tasks"],task_size, task_mINS)         
                    print("cloud response time for", d, "through",closest_candidate, ":", cloud_response_time)
                    resp_times_list.append(cloud_response_time)
                    methods_list.append("Cloud through fog")
            else:
                G.add_edges_from([('C',d)])
                link_attrs = add_link_attributes()
                nx.set_edge_attributes(G, link_attrs)

                c2d_distance = calculateDistance(node_pos[d][0], node_pos[d][1],node_positions["C"][0],node_positions["C"][1])
                cloud_device_distance = [('C',d, c2d_distance )]
                cloud_direct_time = Calculate_Response_Time(d,'C', None, cloud_device_distance, G.nodes[d]["Tasks"],task_size, task_mINS)

                print("App in", d, "is sent directly to Cloud with response time", cloud_direct_time)
                resp_times_list.append(cloud_direct_time)
                methods_list.append("Cloud direct")
    

    endtime = time.time()
    Total_number_of_nodes = G.number_of_nodes()
    Total_number_of_edges = G.number_of_edges()

    
    avg_fogs_inrange_cluster = statistics.mean(inrange_cluster_num_fogs)
    instance_avg_fogs_inrange_cluster.append(avg_fogs_inrange_cluster)

    avg_fogs_neighbor_cluster = statistics.mean(neighbor_cluster_num_fogs)
    instance_avg_fogs_neighbor_cluster.append(avg_fogs_neighbor_cluster)
    
    print(nx.info(G))
    print("avg fogs inrange cluster", instance_avg_fogs_inrange_cluster)
    print("avg fogs neighbor cluster", instance_avg_fogs_neighbor_cluster)

    runtime =  endtime - starttime
    final_runtime.append(runtime)
    print("Runtime:", runtime)
    storeResults(devices_list, resp_times_list, methods_list, Total_number_of_nodes, Total_number_of_edges, runtime, optimizer, suffix)


avg_runtime = statistics.mean(final_runtime)
runtime_deviation = statistics.stdev(final_runtime)
average = getFileAverage()
final_avg, responsetime_deviation  = getAverage(average)
total_avg_fogs_inrange_cluster = statistics.mean(instance_avg_fogs_inrange_cluster)
total_avg_fogs_neighbor_cluster = statistics.mean(instance_avg_fogs_neighbor_cluster)

print("average runtime:", avg_runtime)
print("runtime_deviation:", runtime_deviation)
print ("response times averages:", final_avg)
print("response times deviation:", responsetime_deviation)
print("total average fogs inrange cluster", total_avg_fogs_inrange_cluster)
print("total average fogs neighbor cluster", total_avg_fogs_neighbor_cluster)

#plotGraph()

file = "C:/Users/Hassan/Documents/MIRI/Final_Thesis/NetworkX/test_results.txt" 

with open(file, 'w') as f:
    f.writelines("average runtime = " + str(avg_runtime) + '\n')
    f.writelines("runtimes STD = " + str(runtime_deviation) + '\n')
    f.writelines("average response times = " + str(final_avg) + '\n')
    f.writelines("response times STD = " + str(responsetime_deviation) + '\n')
    f.writelines("total average fogs inrange cluster = " + str(total_avg_fogs_inrange_cluster) + '\n')
    f.writelines("total average fogs neighbor cluster = " + str(total_avg_fogs_neighbor_cluster) + '\n')

