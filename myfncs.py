import networkx as nx
import matplotlib.pyplot as plt



def add_nodes_to(node, number, ntype):
    l =[]
    for item in range(1,number+1):
        item = ntype + str(item)
        t = (node, item)
        l.append(t) 
    return l

# print(add_nodes_to("cloud", 3, "fog"))