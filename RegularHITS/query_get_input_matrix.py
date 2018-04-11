import numpy as np
from collections import deque


def query_get_input_matrix(dataset, query_node_index=249080, N=3):

    """
    Step 3: Get input adjacency matrices from the subgraph given the query node.
    """

    # Load the data graph (The reason we don't consider customer nodes is that they cause high bias in the subgraph nodes)
    data = np.load(dataset).item()
    adjacency_matrix = data["adjacency_matrix"]
    # print type(adjacency_matrix)  # <class 'scipy.sparse.csr.csr_matrix'>

    # data = adjacency_matrix.data
    indices = adjacency_matrix.indices
    indptr = adjacency_matrix.indptr

    # BFS (N-step subgraph)
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

    # Get input for multi-layered HITS algorithm according to correspondent layers
    layers = ["book", "dvd", "music", "video"]

    temp = {"subgraph_indices_book": [], "subgraph_indices_dvd": [], "subgraph_indices_music": [], "subgraph_indices_video": []}
    for idx in subgraph_node_indices:
        for l in layers:
            if data["indices_range_" + l][0] <= idx < data["indices_range_" + l][1]:
                temp["subgraph_indices_" + l].append(idx)
                break

    # Get indices range for each group
    indices_range_book = [0, 0 + len(temp["subgraph_indices_book"])]
    indices_range_dvd = [indices_range_book[1], indices_range_book[1] + len(temp["subgraph_indices_dvd"])]
    indices_range_music = [indices_range_dvd[1], indices_range_dvd[1] + len(temp["subgraph_indices_music"])]
    indices_range_video = [indices_range_music[1], indices_range_music[1] + len(temp["subgraph_indices_video"])]

    index2Id = {}
    for l in layers:
        index2Id[l] = data['index2Id_' + l][np.array(temp["subgraph_indices_" + l], dtype=int) - int(data["indices_range_" + l][0])]

    subgraph_data = {
        "adjacency_matrix": adjacency_matrix[subgraph_node_indices, :].tocsc()[:, subgraph_node_indices],

        "indices_range_book": np.array(indices_range_book),
        "indices_range_dvd": np.array(indices_range_dvd),
        "indices_range_music": np.array(indices_range_music),
        "indices_range_video": np.array(indices_range_video),

        "index2Id_book": np.array(index2Id["book"]),
        "index2Id_dvd": np.array(index2Id["dvd"]),
        "index2Id_music": np.array(index2Id["music"]),
        "index2Id_video": np.array(index2Id["video"]),
    }

    return subgraph_data
