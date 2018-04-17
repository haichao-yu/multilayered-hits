# import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix, rand
# from loss_func import loss_func_regular


def regular_hits(A, iteration_times=40):
    """
    Regular HITS Algorithm
    :param A: Adjacency matrix
    :param iteration_times: Iteration times
    :return: Authority scores and Hub scores
    """

    print("\nRegular HITS algorithm is started.")

    epsilon = 1e-10  # A very small constant to avoid denominator becomes 0

    '''
    Initialize authority score and hub score
    '''
    u = rand(A.shape[0], 1, density=1, format='csc')
    v = rand(A.shape[0], 1, density=1, format='csc')

    '''
    NMF: multiplicative update u and v
    '''
    J_list = []
    for t in range(iteration_times):

        u_numerator = (A / float(A.sum() + epsilon)).dot(v)
        u_denominator = u.dot((v.transpose()).dot(v))
        v_numerator = u.transpose().dot(A / float(A.sum() + epsilon))
        v_denominator = u.transpose().dot(u).dot(v.transpose())

        u_numerator = csc_matrix(u_numerator.todense() + epsilon)
        u_denominator = csc_matrix(u_denominator.todense() + epsilon)
        next_u = u.multiply(csc_matrix(u_numerator / u_denominator).sqrt())

        v_numerator = csc_matrix(v_numerator.todense() + epsilon)
        v_denominator = csc_matrix(v_denominator.todense() + epsilon)
        next_v_transpose = v.transpose().multiply(csc_matrix(v_numerator / v_denominator).sqrt())

        u = next_u
        v = next_v_transpose.transpose()

        # J_list.append(loss_func_regular(A, u, v))

        print("The %03dth iteration is completed." % (t + 1))

    print("Regular HITS algorithm is completed.\n")

    # Draw figure: cost w.r.t iteration
    # plt.figure()
    # plt.title("Cost w.r.t Iteration")
    # plt.xlabel("Iteration")
    # plt.ylabel("Cost")
    # plt.plot(range(1, iteration_times + 1), J_list, label="J")
    # plt.show()

    return [u, v]
