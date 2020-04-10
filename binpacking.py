from pulp import *
from collections import Counter

def linear_programming_solver(task_list, task_count, fog_names, fogs_ram, cost):
    y = pulp.LpVariable.dicts('BinUsed', range(len(fog_names)), lowBound=0, upBound=1, cat=pulp.LpInteger)
    possible_ItemInBin = [(itemTuple[0], binNum) for itemTuple in task_list for binNum in range(len(fog_names))]
    x = pulp.LpVariable.dicts('itemInBin', possible_ItemInBin, lowBound=0, upBound=1, cat=pulp.LpInteger)

    # Model formulation
    prob = LpProblem("Bin Packing Problem", LpMinimize)

    # Objective
    prob += lpSum([cost[i] * y[i] for i in range(len(fog_names))])

    # Constraints
    for j in task_list:
        prob += lpSum([x[(j[0], i)] for i in range(len(fog_names))]) == 1
    for i in range(len(fog_names)):
        prob += lpSum([task_list[j][1] * x[(task_list[j][0], i)] for j in range(task_count)]) <= fogs_ram[i] * y[i]
    prob.solve()  
    #print("Fog nodes used: " + str(sum(([y[i].value() for i in range(len(fog_names))]))))
    task_number = []
    for i in x.keys(): 
        if x[i].value() == 1:
            task_number.append(i)

    counts = Counter(x[1] for x in (task_number))
    task_assignment = []
    for a, b in counts.items():   
        task_assignment.append((b, fog_names[a]))    
    return task_assignment   
    


