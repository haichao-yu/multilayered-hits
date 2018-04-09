import sys
import getopt
import numpy as np
from terminaltables import AsciiTable  # https://robpol86.github.io/terminaltables/index.html
from load_mat_data import load_mat_data
from ranking_get_input_matrices import ranking_get_input_matrices
from query_get_input_matrices import query_get_input_matrices
from multilayered_hits import multilayered_hits
from get_collection_from_db import get_collection_from_db


"""
mu = 0.1
iteration_times = 100
[G, A, D] = load_mat_data("../AmazonDataProcessing/datasets/ItalyInfra.mat")
[u, v] = multilayered_hits(G, A, D, mu, iteration_times)
"""


"""
test query node indices: 4228, 12736, 17395, 18110, 20570, 31807, 41744, 87951, 93818, 125918, 165080, 176185, 280878
"""


def display_help():
    print "Welcome, this is a program of Multi-layered HITS."
    print ""
    print "All experiments are based on the dataset of Amazon Co-purchasing Network and its metadata."
    print ""
    print "python __init__.py [option value]"
    print ""
    print "Option and arguments:"
    print "-t or --task             The task to execute: 0 represent ranking, 1 represent query."
    print "                         * ranking requires arguments of \"selected_layers\";"
    print "                         * query requires arguments of \"query_node_index\" and \"N\";"
    print "--selected_layers        The layers selected for ranking task, separated by ',':"
    print "                         * 4 data layers (book, dvd, music, video);"
    print "                         * 1 knowledge layer (customer);"
    print "--query_node_index       The query node for query task."
    print "--N                      The K-step subgraph for query task."
    print "--mu                     The regularization parameter for cross-layer consistency, default is 1."
    print "--iteration_times        The iteration times for the algorithm, default is 100."
    print ""
    print "Ranking example:"
    print "python __init__.py -t 0 --selected_layers book,dvd,music,video,customer"
    print ""
    print "Query example:"
    print "python __init__.py -t 1 --query_node 4228 --N 3 --iteration_times 20"


if __name__ == '__main__':

    DATA_LAYERS = ("Book", "DVD", "Music", "Video")
    PRODUCT_LINK_PREFIX = "www.amazon.com/gp/product/"
    K = 10  # top K products

    products = get_collection_from_db()  # product collection

    mu = 0.1  # regularization parameter
    iteration_times = 100

    task = None  # 0 for ranking, 1 for query

    selected_layers = None  # ranking parameter
    query_node_index = None  # query parameter
    N = None  # query parameter

    opts, args = getopt.getopt(sys.argv[1:], "ht:", ["help", "task=", "selected_layers=", "query_node_index=", "N=", "mu=", "iteration_times="])

    if len(opts) == 0:
        display_help()
        exit(0)

    for option, value in opts:
        if option == "-h" or option == "--help":
            display_help()
            exit(0)
        elif option == "-t" or option == "--task":
            task = int(value)
            if task != 0 and task != 1:
                print "Invalid option or value! Please try again."
                exit(0)
        elif option == "--selected_layers":
            selected_layers = value.split(',')
        elif option == "--query_node_index":
            query_node_index = int(value)
        elif option == "--N":
            N = int(value)
        elif option == "--mu":
            mu = float(value)
        elif option == "--iteration_times":
            iteration_times = int(value)
        else:
            print "Invalid option or value! Please try again."
            exit(0)

    if task is None:
        print "Invalid option or value! Please try again."
        exit(0)

    if task == 0:  # ranking
        if selected_layers is None:
            print "You need to specify the selected layers! Please try again."
            exit(0)
        data = ranking_get_input_matrices(selected_layers)

        # print data["GroupNet"]
        # print data["GroupDict"]
        # print data["WithinLayerNets"]
        # print data["WithinLayerNetsDict"]
        # print data["CrossLayerDependencies"]

        G = data["GroupNet"]
        A = data["WithinLayerNets"]
        D = data["CrossLayerDependencies"]
        [u, v] = multilayered_hits(G, A, D, mu, iteration_times)

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
        for i, g in enumerate(data["GroupDict"]):
            # print u[i].todense().getA1()
            # print v[i].todense().getA1()
            index2Id = data["WithinLayerNetsDict"][i]
            rank_ui = np.flip(np.argsort(u[i].todense().getA1()), axis=0)
            rank_vi = np.flip(np.argsort(v[i].todense().getA1()), axis=0)
            for rank, index in enumerate(rank_ui):
                record = products.find_one({"Id": int(index2Id[index])})
                top_K_products_authority[g].append([rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"], record["salesrank"]])
                if len(top_K_products_authority[g]) > K:
                    break
            table = AsciiTable(top_K_products_authority[g])
            table.title = "Top " + str(K) + " relevant " + g + "s (Authority)"
            print table.table
            for rank, index in enumerate(rank_vi):
                record = products.find_one({"Id": int(index2Id[index])})
                top_K_products_hub[g].append([rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"], record["salesrank"]])
                if len(top_K_products_hub[g]) > K:
                    break
            table = AsciiTable(top_K_products_hub[g])
            table.title = "Top " + str(K) + " relevant " + g + "s (Hub)"
            print table.table
            print ""

    else:  # task == 1  # query
        if query_node_index is None or N is None:
            print "You need to specify the query node index and the N parameter! Please try again."
            exit(0)
        data = query_get_input_matrices(query_node_index, N)

        # print data["QueryProductId"]
        # print data["GroupNet"]
        # print data["GroupDict"]
        # print data["WithinLayerNets"]
        # print data["WithinLayerNetsDict"]
        # print data["CrossLayerDependencies"]

        G = data["GroupNet"]
        A = data["WithinLayerNets"]
        D = data["CrossLayerDependencies"]
        [u, v] = multilayered_hits(G, A, D, mu, iteration_times)

        record = products.find_one({"Id": data["QueryProductId"]})
        table = AsciiTable([[record["group"], record["title"], PRODUCT_LINK_PREFIX + record["ASIN"]]])
        table.title = "The query product"
        print table.table
        print ""

        top_K_products_authority = {
            "book": [["Rank", "Product", "Link", "Rating"]],
            "dvd": [["Rank", "Product", "Link", "Rating"]],
            "music": [["Rank", "Product", "Link", "Rating"]],
            "video": [["Rank", "Product", "Link", "Rating"]]
        }
        top_K_products_hub = {
            "book": [["Rank", "Product", "Link", "Rating"]],
            "dvd": [["Rank", "Product", "Link", "Rating"]],
            "music": [["Rank", "Product", "Link", "Rating"]],
            "video": [["Rank", "Product", "Link", "Rating"]]
        }
        for i, g in enumerate(data["GroupDict"]):
            # print u[i].todense().getA1()
            # print v[i].todense().getA1()
            index2Id = data["WithinLayerNetsDict"][i]
            rank_ui = np.flip(np.argsort(u[i].todense().getA1()), axis=0)
            rank_vi = np.flip(np.argsort(v[i].todense().getA1()), axis=0)
            for rank, index in enumerate(rank_ui):
                record = products.find_one({"Id": index2Id[index]})
                top_K_products_authority[g].append([rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"]])
                if len(top_K_products_authority[g]) > K:
                    break
            table = AsciiTable(top_K_products_authority[g])
            table.title = "Top " + str(K) + " relevant " + g + "s (Authority)"
            print table.table
            for rank, index in enumerate(rank_vi):
                record = products.find_one({"Id": index2Id[index]})
                top_K_products_hub[g].append([rank + 1, record["title"], PRODUCT_LINK_PREFIX + record["ASIN"]])
                if len(top_K_products_hub[g]) > K:
                    break
            table = AsciiTable(top_K_products_hub[g])
            table.title = "Top " + str(K) + " relevant " + g + "s (Hub)"
            print table.table
            print ""
