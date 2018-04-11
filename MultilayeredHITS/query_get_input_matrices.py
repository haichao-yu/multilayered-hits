import numpy as np
from collections import deque


def query_get_input_matrices(query_node_index=249080, N=3):

    """
    Step 3: Get input adjacency matrices from the subgraph given the query node.
    """

    # Load the data graph (The reason we don't consider customer nodes is that they cause high bias in the subgraph nodes)
    data = np.load("../AmazonDataProcessing/datasets/amazon-data-graph.npy").item()
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
            for neighbor in indices[indptr[i]:indptr[i+1]]:  # col index
                if neighbor not in subgraph_node_indices:
                    subgraph_node_indices.append(neighbor)
                    queue.append(neighbor)
        N -= 1

    # Get input for multi-layered HITS algorithm according to correspondent layers
    layers = ["book", "dvd", "music", "video"]

    temp = {"subgraph_indices_book": [], "subgraph_indices_dvd": [], "subgraph_indices_music": [], "subgraph_indices_video": []}
    for idx in np.sort(subgraph_node_indices):
        for l in layers:
            if data["indices_range_" + l][0] <= idx < data["indices_range_" + l][1]:
                temp["subgraph_indices_" + l].append(idx)
                break

    WithinLayerNets = []
    WithinLayerNetsDict = []
    for l in layers:
        WithinLayerNets.append(adjacency_matrix[temp["subgraph_indices_"+l], :].tocsc()[:, temp["subgraph_indices_"+l]])
        WithinLayerNetsDict.append(data['index2Id_'+l][np.array(temp["subgraph_indices_"+l], dtype=int) - int(data["indices_range_" + l][0])])
    WithinLayerNets = np.array(WithinLayerNets)
    WithinLayerNetsDict = np.array(WithinLayerNetsDict)

    GroupNet = np.zeros((len(layers), len(layers)), dtype=int)
    GroupDict = np.array(layers)
    CrossLayerDependencies = []
    position = 0
    for i in range(len(layers)):
        for j in range(i + 1, len(layers)):
            position += 1
            GroupNet[i, j] = GroupNet[j, i] = position
            CrossLayerDependencies.append(adjacency_matrix[temp["subgraph_indices_"+layers[i]], :].tocsc()[:, temp["subgraph_indices_"+layers[j]]])
    CrossLayerDependencies = np.array(CrossLayerDependencies)

    query_product_id = -1
    for l in layers:
        if data["indices_range_" + l][0] <= query_node_index < data["indices_range_" + l][1]:
            query_product_id = data["index2Id_" + l][query_node_index - data["indices_range_" + l][0]]

    # Return
    subgraph_data = {
        "QueryProductId": query_product_id,
        "GroupNet": GroupNet,
        "GroupDict": GroupDict,
        "WithinLayerNets": WithinLayerNets,
        "WithinLayerNetsDict": WithinLayerNetsDict,
        "CrossLayerDependencies": CrossLayerDependencies,
    }
    return subgraph_data
