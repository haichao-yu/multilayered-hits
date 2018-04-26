import numpy as np
from collections import deque


def subgraph_from_bfs(adjacency_matrix, query_node_index, N=3):

    indices = adjacency_matrix.indices
    indptr = adjacency_matrix.indptr

    subgraph_node_indices = [query_node_index]
    queue = deque([query_node_index])
    while len(queue) > 0 and N > 0:
        size = len(queue)
        for counter in range(size):
            i = queue.popleft()  # row index
            for neighbor in indices[indptr[i]:indptr[i + 1]]:  # col index
                if neighbor not in subgraph_node_indices:
                    subgraph_node_indices.append(neighbor)
                    queue.append(neighbor)
        N -= 1
    subgraph_node_indices = np.sort(subgraph_node_indices)

    return subgraph_node_indices
