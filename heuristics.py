# define a function to take a dictionary sizes with sizes for objects,
# and return a list of sets of objects, where the summed size of the objects in
# each set is <= max_summed_size_per_bin. This is a bin packing problem, and uses
# a simple algorithm, the 'First Fit Decreasing' (FFD) algorithm: first sort
# the items in decreasing orders by their sizes, and then insert each item in
# the first bin in the list with sufficient remaining space.

def first_fit_algorithm(sizes, bins, return_sizes=None):
    """partition objects into bins, where the summed size of objects in a bin is <= max_summed_size_per_bin
    >>> first_fit_algorithm({'task1': 5, 'task2': 4, 'task3': 4, task4: 3, 'task5': 2, 'task6': 2}, [('fog1',1569),('fog2',1667)], return_sizes=True)
    [(2, 'fog1'), (4, 'fog2')]
    """
    # Returns [{'seq1', 'seq2'}, {'seq3', 'seq4', 'seq5'}, {'seq6'}]
    # Note that this algorithm is heuristic and does not give the optimal solution,
    # which is ({'seq2', 'seq3', 'seq5'     }, {'seq1', 'seq4', 'seq6'}]
    # However, optimal bin packing is NP-hard and exact algorithms that do it are complicated.
    fog_task = []
    index = 0
    # insert each object in the first bin with sufficient remaining space:
    for b in bins: # 'my_bin' is a set of objects in a bin
        assigned_task = []
        b_size = b[1]
        b_filled = 0 
        for i in range (index,(len(sizes))):
            object_size = sizes[i][1]                 
            if  b_filled < b_size:
                if object_size <= (b_size - b_filled ):
                   assigned_task.append(i)
                   b_filled = b_filled + object_size
                else:
                   break
        index = i
        fog_task.append((len(assigned_task), b[0]))

    return fog_task

