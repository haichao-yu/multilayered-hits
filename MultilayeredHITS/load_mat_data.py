import scipy.io as sio


def load_mat_data(dataset):
    """
    G: The layer-layer dependency matrix
    A: Within-layer connectivity matrices
    D: Cross-layer dependency matrix
    
    - G[i][j] = 0 means there is no dependency between layer i and layer j;
    - G[i][j] = k means D[k-1] (the kth matrix in D) is the dependency matrix between layer i and layer j;
    """

    print "Loading .mat data ..."

    data = sio.loadmat(dataset)

    G = data['G']
    A = [data['A'][0, i][0, 0][0] for i in range(data['A'].shape[1])]
    D = [data['D'][0, i][0, 0][0] for i in range(data['D'].shape[1])]

    print "The data is successfully loaded."

    return [G, A, D]
