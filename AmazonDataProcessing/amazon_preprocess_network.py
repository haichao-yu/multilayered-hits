import gzip
import json
import numpy as np
import networkx as nx


def amazon_preprocess_network():
    """
    Step 2: - Read the product co-purchasing network (http://snap.stanford.edu/data/com-Amazon.html) as data graph;
            - Combine knowledge graph (customers/reviews) with the data graph;
            - Extract data+knowledge graph and save its adjacency matrix;
    """

    print "Start preprocessing amazon network."

    # Read product info from processed json file
    with gzip.open("./datasets/amazon-products.json.gz", "rb") as f:
        products = json.loads(f.read().decode("ascii"))

    # Represent amazon product co-purchasing network (http://snap.stanford.edu/data/com-Amazon.html) as a networkx graph object (node is product Id)
    G = nx.read_edgelist("./datasets/com-amazon.ungraph.txt.gz", nodetype=int)

    # Remove nodes that don't belong to any of Book, DVD, Music, Video
    nodes_to_remove = []
    for node in G.nodes():
        if products[node]["group"] != "Book" and products[node]["group"] != "DVD" and products[node]["group"] != "Music" and products[node]["group"] != "Video":
            nodes_to_remove.append(node)
    G.remove_nodes_from(nodes_to_remove)
    print G.number_of_nodes()   # 334844
    print G.number_of_edges()   # 925803

    # Get nodes for each group (Book, DVD, Music, Video)
    nodes_book = []
    nodes_dvd = []
    nodes_music = []
    nodes_video = []

    for node in G.nodes():
        if products[node]["group"] == "Book":
            nodes_book.append(node)
        elif products[node]["group"] == "DVD":
            nodes_dvd.append(node)
        elif products[node]["group"] == "Music":
            nodes_music.append(node)
        else:  # "Video"
            nodes_video.append(node)
    print len(nodes_book)           # 248916
    print len(nodes_dvd)            # 15743
    print len(nodes_music)          # 54824
    print len(nodes_video)          # 15361

    # Get indices range for each group
    indices_range_book = [0, 0 + len(nodes_book)]
    indices_range_dvd = [indices_range_book[1], indices_range_book[1] + len(nodes_dvd)]
    indices_range_music = [indices_range_dvd[1], indices_range_dvd[1] + len(nodes_music)]
    indices_range_video = [indices_range_music[1], indices_range_music[1] + len(nodes_video)]

    # Save the data (Without knowledge layer - customers)
    # data = {
    #     "adjacency_matrix": nx.adjacency_matrix(G, nodelist=(nodes_book + nodes_dvd + nodes_music + nodes_video)),
    #
    #     "indices_range_book": np.array(indices_range_book),
    #     "indices_range_dvd": np.array(indices_range_dvd),
    #     "indices_range_music": np.array(indices_range_music),
    #     "indices_range_video": np.array(indices_range_video),
    #
    #     "index2Id_book": np.array(nodes_book),
    #     "index2Id_dvd": np.array(nodes_dvd),
    #     "index2Id_music": np.array(nodes_music),
    #     "index2Id_video": np.array(nodes_video),
    # }
    # np.save("./datasets/amazon-data-graph.npy", data)

    # Knowledge layer: customers (the edge between product and customer is review)
    product_customer_edges = []
    for node in G.nodes():
        for r in products[node]["reviews"]:
            if float(r["rating"]) >= 4.0 and int(r["votes"] >= 20 and float(r["helpful"])/float(r["votes"]) >= 0.8):  # filter reviews
                product_customer_edges.append((node, r["customer"]))
    G.add_edges_from(product_customer_edges)

    nodes_customer = []
    for node in G.nodes():
        if not isinstance(node, int):
            nodes_customer.append(node)
    indices_range_customers = [indices_range_video[1], indices_range_video[1] + len(nodes_customer)]
    print len(nodes_customer)       # 64608

    # Knowledge layer: categories (nodes are categories)
    product_category_edges = []
    nodes_categories = []
    for node in (nodes_book + nodes_dvd + nodes_music + nodes_video):
        for c in products[node]["categories"]:
            product_category_edges.append((node, c))
            if c not in nodes_categories:
                nodes_categories.append(c)
    G.add_edges_from(product_category_edges)
    indices_range_categories = [indices_range_customers[1], indices_range_customers[1] + len(nodes_customer)]
    print len(nodes_categories)     # 73

    # Save the data (With knowledge layer - customers)
    data = {
        "adjacency_matrix": nx.adjacency_matrix(G, nodelist=(nodes_book + nodes_dvd + nodes_music + nodes_video + nodes_customer + nodes_categories)),

        "indices_range_book": np.array(indices_range_book),
        "indices_range_dvd": np.array(indices_range_dvd),
        "indices_range_music": np.array(indices_range_music),
        "indices_range_video": np.array(indices_range_video),
        "indices_range_customer": np.array(indices_range_customers),
        "indices_range_categories": np.array(indices_range_categories),

        "index2Id_book": np.array(nodes_book),
        "index2Id_dvd": np.array(nodes_dvd),
        "index2Id_music": np.array(nodes_music),
        "index2Id_video": np.array(nodes_video),
        "index2Id_customer": np.array(nodes_customer),
        "index2Id_categories": np.array(nodes_categories),
    }
    np.save("./datasets/amazon-data-knowledge-graph.npy", data)

    print "Finish preprocessing amazon network."
