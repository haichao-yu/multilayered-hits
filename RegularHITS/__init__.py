import numpy as np
from terminaltables import AsciiTable  # https://robpol86.github.io/terminaltables/index.html
from ranking_get_input_matrix import ranking_get_input_matrix
from regular_hits import regular_hits
from get_collection_from_db import get_collection_from_db

if __name__ == '__main__':

    products = get_collection_from_db()

    DATA_LAYERS = ("book", "dvd", "music", "video")
    PRODUCT_LINK_PREFIX = "www.amazon.com/gp/product/"
    K = 5  # top K products

    dataset = "../AmazonDataProcessing/datasets/amazon-data-graph.npy"
    # dataset = "../AmazonDataProcessing/datasets/amazon-data-knowledge-graph.npy"
    iteration_times = 40

    data = ranking_get_input_matrix(dataset)
    A = data['adjacency_matrix']
    # print adjacency_matrix.shape
    [u, v] = regular_hits(A, iteration_times)

    top_K_products_authority = {
        "book": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "dvd": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "music": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "video": [["Rank", "Product", "Link", "Salesrank", "Rating"]]
    }
    top_K_products_hub = {
        "book": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "dvd": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "music": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "video": [["Rank", "Product", "Link", "Salesrank", "Rating"]]
    }

    for g in DATA_LAYERS:
        ui = u[data['indices_range_' + g][0]:data['indices_range_' + g][1], 0]
        vi = v[data['indices_range_' + g][0]:data['indices_range_' + g][1], 0]
        rank_ui = np.flip(np.argsort(ui.todense().getA1()), axis=0)
        rank_vi = np.flip(np.argsort(vi.todense().getA1()), axis=0)
        for rank, index in enumerate(rank_ui):
            record = products.find_one({"Id": int(data['index2Id_' + g][index])})
            top_K_products_authority[g].append(
                [rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"], record["salesrank"]])
            if len(top_K_products_authority[g]) > K:
                break
        table = AsciiTable(top_K_products_authority[g])
        table.title = "Top " + str(K) + " relevant " + g + "s (Authority)"
        print table.table
        for rank, index in enumerate(rank_vi):
            record = products.find_one({"Id": int(data['index2Id_' + g][index])})
            top_K_products_hub[g].append(
                [rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"], record["salesrank"]])
            if len(top_K_products_hub[g]) > K:
                break
        table = AsciiTable(top_K_products_hub[g])
        table.title = "Top " + str(K) + " relevant " + g + "s (Hub)"
        print table.table
        print ""
