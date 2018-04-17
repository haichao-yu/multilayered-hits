# import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix, rand, diags
# from loss_func import loss_func_multilayered


def multilayered_hits(G, A, D, mu=0.1, iteration_times=20):
    """
    Multilayered-HITS Algorithm
    :param G: The layer-layer dependency matrix
    :param A: Within-layer connectivity matrices
    :param D: Cross-layer dependency matrix
    :param iteration_times: Iteration times
    :param mu: Weight of cross-layer consistency
    :return: Authority scores and Hub scores for each layer
    """

    print("\nMultilayered HITS algorithm is started.")

    epsilon = 1e-10  # A very small constant to avoid denominator becomes 0

    '''
    Initialize authority score and hub score for all layers
    '''
    u = []  # Authority score
    v = []  # Hub score
    for Ai in A:
        ui = rand(Ai.shape[0], 1, density=1, format='csc')
        vi = rand(Ai.shape[0], 1, density=1, format='csc')
        u.append(ui)
        v.append(vi)

    '''
    NMF: multiplicative update ui and vi
    '''
    J_list = []
    for t in range(iteration_times):

        next_u = []
        next_v = []
        for i in range(G.shape[0]):

            # Within-layer
            ui_numerator = (A[i] / float(A[i].sum() + epsilon)).dot(v[i])
            ui_denominator = u[i].dot((v[i].transpose()).dot(v[i]))
            vi_numerator = u[i].transpose().dot(A[i] / float(A[i].sum() + epsilon))
            vi_denominator = u[i].transpose().dot(u[i]).dot(v[i].transpose())

            # Cross-layer
            for j in range(G.shape[1]):

                # There is no dependency between layer i and layer j
                if i == j or int(G[i, j]) == 0:
                    continue

                # There is a dependency (matrix Dij) between layer i and layer j
                Dij = D[int(G[i, j]) - 1]
                if Dij.shape[0] != u[i].shape[0]:
                    Dij = Dij.transpose()
                assert Dij.shape[0] == u[i].shape[0] and Dij.shape[1] == u[j].shape[0]

                # Get the diagonal degree matrix of Dij
                degree_Dij = diags(Dij.sum(axis=1).A1)

                # Append cross-layers terms
                ui_numerator += 2 * mu * (Dij.dot(u[j]))
                ui_denominator += 2 * mu * (degree_Dij.dot(u[i]))

                vi_numerator += 2 * mu * (v[j].transpose().dot(Dij.transpose()))
                vi_denominator += 2 * mu * (v[i].transpose().dot(degree_Dij.transpose()))

            # Compute the values of next ui and next vi
            ui_numerator = csc_matrix(ui_numerator.todense() + epsilon)
            ui_denominator = csc_matrix(ui_denominator.todense() + epsilon)
            next_ui = u[i].multiply(csc_matrix(ui_numerator / ui_denominator).sqrt())
            next_u.append(next_ui)

            vi_numerator = csc_matrix(vi_numerator.todense() + epsilon)
            vi_denominator = csc_matrix(vi_denominator.todense() + epsilon)
            next_vi_transpose = v[i].transpose().multiply(csc_matrix(vi_numerator / vi_denominator).sqrt())
            next_v.append(next_vi_transpose.transpose())

        # Update
        u = next_u
        v = next_v

        # J_list.append(loss_func_multilayered(G, A, D, u, v, mu))

        print("The %03dth iteration is completed." % (t + 1))

    print("Multilayered HITS algorithm is completed.\n")

    # Draw figure: cost w.r.t iteration
    # plt.figure()
    # plt.title("Cost w.r.t Iteration")
    # plt.xlabel("Iteration")
    # plt.ylabel("Cost")
    # plt.plot(range(1, iteration_times + 1), J_list, label="J")
    # plt.show()

    return [u, v]
