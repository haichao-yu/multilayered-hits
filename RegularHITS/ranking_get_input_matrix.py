import numpy as np


def ranking_get_input_matrix(dataset):

    data = np.load(dataset).item()
    adjacency_matrix = data["adjacency_matrix"]
    index2Id = data["index2Id"]

    return [adjacency_matrix, index2Id]
