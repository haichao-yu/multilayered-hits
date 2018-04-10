from scipy.sparse import diags
from scipy.sparse.linalg import norm


def loss_func(G, A, D, u, v, mu):
    """
    Loss Function
    :param G: The layer-layer dependency matrix
    :param A: Within-layer connectivity matrices
    :param D: Cross-layer dependency matrix
    :param u: Authority score for each layer
    :param v: Hub score for each layer
    :return: cost
    """

    cost = 0
    for i in range(G.shape[0]):

        # Within-layer smoothness
        # cost += 0.5 * norm(A[i] / float(A[i].sum() + 1e-10) - u[i].dot(v[i].transpose())) ** 2
        cost += 0.5 * (1 / float(A[i].sum() + 1e-10) ** 2) * A[i].dot(A[i].transpose()).diagonal().sum() - (u[i].transpose().dot((A[i] / float(A[i].sum() + 1e-10)).dot(v[i])))[0, 0] + 0.5 * ((u[i].transpose().dot(u[i])) * (v[i].transpose().dot(v[i])))[0, 0]

        # Cross-layer consistency
        for j in range(G.shape[1]):

            # There is no dependency between layer i and layer j
            if i == j or int(G[i, j]) == 0:
                continue

            # There is a dependency (matrix Dij) between layer i and layer j
            Dij = D[int(G[i, j]) - 1]
            if Dij.shape[0] != u[i].shape[0]:
                Dij = Dij.transpose()
            assert Dij.shape[0] == u[i].shape[0] and Dij.shape[1] == u[j].shape[0]
            Dji = Dij.transpose()

            # Get the diagonal degree matrix of Dij and Dji
            degree_Dij = diags(Dij.sum(axis=1).A1)
            degree_Dji = diags(Dji.sum(axis=1).A1)

            cost += mu * (u[i].transpose().dot(degree_Dij).dot(u[i]) + u[i].transpose().dot(-Dij).dot(u[j]) + u[j].transpose().dot(-Dji).dot(u[i]) + u[j].transpose().dot(degree_Dji).dot(u[j]))[0, 0]
            cost += mu * (v[i].transpose().dot(degree_Dij).dot(v[i]) + v[i].transpose().dot(-Dij).dot(v[j]) + v[j].transpose().dot(-Dji).dot(v[i]) + v[j].transpose().dot(degree_Dji).dot(v[j]))[0, 0]

    return cost
