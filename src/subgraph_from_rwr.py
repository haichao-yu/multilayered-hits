import random
import numpy as np


def subgraph_from_rwr(adjacency_matrix, query_node_index, size=500, alpha=0.7):
    """ 
    :param size: size of subgraph 
    :param alpha: probability of restart
    """

    indices = adjacency_matrix.indices
    indptr = adjacency_matrix.indptr

    rand = random.Random()
    path = [query_node_index]
    subgraph_node_indices = [query_node_index]
    while len(subgraph_node_indices) < size:
        curr_node = path[-1]
        if len(indices[indptr[curr_node]:indptr[curr_node + 1]]) > 0:
            if rand.random() >= alpha:
                next_node = rand.choice(indices[indptr[curr_node]:indptr[curr_node + 1]])
                path.append(next_node)
                if next_node not in subgraph_node_indices:
                    subgraph_node_indices.append(next_node)
            else:
                path.append(path[0])
        else:
            break
    subgraph_node_indices = np.sort(subgraph_node_indices)

    return subgraph_node_indices
