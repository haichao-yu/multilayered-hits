import gzip
import json
import numpy as np
import networkx as nx


def amazon_preprocess_network():

    """
    Step 2: - Read the data graph (product co-purchasing network) and save its adjacency matrix (for querying);
              <http://snap.stanford.edu/data/com-Amazon.html>
            - Combine knowledge graph (customers/reviews) with the data graph;
            - Extract data+knowledge graph and save its adjacency matrix (for ranking);
    """

    print "Start preprocessing amazon network."

    # Read product info from processed json file
    with gzip.open("./datasets/amazon-products.json.gz", "rb") as f:
        products = json.loads(f.read().decode("ascii"))

    # Represent amazon product co-purchasing network (http://snap.stanford.edu/data/com-Amazon.html) as a networkx graph obj (node is product Id)
    G = nx.read_edgelist("./datasets/com-amazon.ungraph.txt.gz", nodetype=int)

    # Remove nodes that don't belong to any of Book, DVD, Music, Video
    nodes_to_remove = []
    for node in G.nodes():
        if products[node]["group"] != "Book" and products[node]["group"] != "DVD" and products[node]["group"] != "Music" and products[node]["group"] != "Video":
            nodes_to_remove.append(node)
    G.remove_nodes_from(nodes_to_remove)
    # print G.number_of_nodes()   # 334844
    # print G.number_of_edges()   # 925803

    # Get indices for each layer (Book, DVD, Music, Video) and the index2id dictionay
    indices_book = []
    indices_dvd = []
    indices_music = []
    indices_video = []

    index2Id = []

    for idx, node in enumerate(G.nodes()):
        if products[node]["group"] == "Book":
            indices_book.append(idx)
        elif products[node]["group"] == "DVD":
            indices_dvd.append(idx)
        elif products[node]["group"] == "Music":
            indices_music.append(idx)
        else:  # "Video"
            indices_video.append(idx)
        index2Id.append(node)
    # print len(indices_book)     # 248916
    # print len(indices_dvd)      # 15743
    # print len(indices_music)    # 54824
    # print len(indices_video)    # 15361
    # print len(index2Id)         # 334844

    # Save the data (Without knowledge layer - customers)
    data = {
        "adjacency_matrix": nx.adjacency_matrix(G),

        "indices_book": np.array(indices_book),
        "indices_dvd": np.array(indices_dvd),
        "indices_music": np.array(indices_music),
        "indices_video": np.array(indices_video),

        "index2Id": np.array(index2Id),
    }
    np.save("./datasets/amazon-data-graph.npy", data)

    # Knowledge layer: customers (the edge between product and customer is review)
    product_customer_edges = []
    for node in G.nodes():
        for r in products[node]["reviews"]:
            if float(r["rating"]) >= 4.0:  # only consider reviews whose rating >= 4
                product_customer_edges.append((node, r["customer"]))
    G.add_edges_from(product_customer_edges)

    Ids_customer = []  # Ids_knowledge
    for node in G.nodes():
        if not isinstance(node, int):
            Ids_customer.append(node)
    # print len(Ids_customer)     # 1144145

    # Save the data (With knowledge layer - customers)
    index2Id += Ids_customer
    data = {
        "adjacency_matrix": nx.adjacency_matrix(G, nodelist=(index2Id)),

        "indices_book": np.array(indices_book),
        "indices_dvd": np.array(indices_dvd),
        "indices_music": np.array(indices_music),
        "indices_video": np.array(indices_video),
        "indices_customer": np.array(range(len(index2Id) - len(Ids_customer), len(index2Id))),

        "index2Id": np.array(index2Id),
    }
    np.save("./datasets/amazon-data-knowledge-graph.npy", data)

    # print len(index2Id)         # 1478989

    print "Finish preprocessing amazon network."
