import numpy as np


def ranking_get_input_matrix(dataset):
    data = np.load(dataset).item()
    return data
