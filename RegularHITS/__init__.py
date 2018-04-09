import numpy as np
from terminaltables import AsciiTable  # https://robpol86.github.io/terminaltables/index.html
from ranking_get_input_matrix import ranking_get_input_matrix
from regular_hits import regular_hits
from get_collection_from_db import get_collection_from_db

if __name__ == '__main__':

    DATA_LAYERS = ("Book", "DVD", "Music", "Video")
    PRODUCT_LINK_PREFIX = "www.amazon.com/gp/product/"
    K = 5  # top K products

    dataset = "../AmazonDataProcessing/datasets/amazon-data-graph.npy"
    # dataset = "../AmazonDataProcessing/datasets/amazon-data-knowledge-graph.npy"
    iteration_times = 40

    [A, index2Id] = ranking_get_input_matrix(dataset)
    # print adjacency_matrix.shape
    [u, v] = regular_hits(A, iteration_times)

    rank_u = np.flip(np.argsort(u.todense().getA1()), axis=0)
    rank_v = np.flip(np.argsort(v.todense().getA1()), axis=0)

    products = get_collection_from_db()

    top_K_products_authority = {
        "Book": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "DVD": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "Music": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "Video": [["Rank", "Product", "Link", "Salesrank", "Rating"]]
    }
    for rank, index in enumerate(rank_u):
        record = products.find_one({"Id": index2Id[index]})
        if record is None:
            continue
        top_K_products_authority[record["group"]].append([rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"], record["salesrank"]])
        if len(top_K_products_authority["Book"]) > K and len(top_K_products_authority["DVD"]) > K and len(top_K_products_authority["Music"]) > K and len(top_K_products_authority["Video"]) > K:
            break

    top_K_products_hub = {
        "Book": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "DVD": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "Music": [["Rank", "Product", "Link", "Salesrank", "Rating"]],
        "Video": [["Rank", "Product", "Link", "Salesrank", "Rating"]]
    }
    for rank, index in enumerate(rank_v):
        record = products.find_one({"Id": index2Id[index]})
        if record is None:
            continue
        top_K_products_hub[record["group"]].append([rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"], record["salesrank"]])
        if len(top_K_products_hub["Book"]) > K and len(top_K_products_hub["DVD"]) > K and len(top_K_products_hub["Music"]) > K and len(top_K_products_hub["Video"]) > K:
            break

    for g in DATA_LAYERS:
        top_K_products_authority[g] = top_K_products_authority[g][0:K+1]
        table = AsciiTable(top_K_products_authority[g])
        table.title = "Top " + str(K) + " " + g + "s (Authority)"
        print table.table
        top_K_products_hub[g] = top_K_products_hub[g][0:K + 1]
        table = AsciiTable(top_K_products_hub[g])
        table.title = "Top " + str(K) + " " + g + "s (Hub)"
        print table.table
        print ""
