import os
import gzip
import shutil
import json
from collections import OrderedDict


def amazon_mata2json():
    """
    Step 1: Preprocess amazon meta data (http://snap.stanford.edu/data/amazon-meta.html) to a json file
    """

    print "Start preprocessing the amazon product metadata to a json file."

    file_amazon_metadata = gzip.open("./datasets/amazon-meta.txt.gz")

    Ids = []
    ASINs = []
    titles = []
    groups = []
    salesranks = []
    avg_ratings = []
    reviews = []

    while True:

        line = file_amazon_metadata.readline()
        if not line:
            break
        items = line.strip().split(" ")
        items = [x for x in items if x != '']  # remove ''

        if len(items) == 0:
            continue

        if items[0] == "Id:":
            Ids.append(int(items[1]))
        if items[0] == "ASIN:":
            ASINs.append(items[1])
        if items[0] == "title:":
            while len(titles) < len(ASINs) - 1:
                titles.append("N/A")
            title = ""
            for w in items[1:]:
                title += (w + " ")
            title = title[0:-1]
            titles.append(title)
        if items[0] == "group:":
            while len(groups) < len(ASINs) - 1:
                groups.append("N/A")
            groups.append(items[1])
        if items[0] == "salesrank:":
            while len(salesranks) < len(ASINs) - 1:
                salesranks.append(-1)
            salesranks.append(int(items[1]))
        if items[0] == "reviews:":
            while len(reviews) < len(ASINs) - 1:
                reviews.append([])
                avg_ratings.append(0.0)
            numOfReviews = int(items[4])  # number of downloaded reviews
            avg_ratings.append(float(items[-1]))

            rlist = []
            if numOfReviews > 0:
                for i in range(numOfReviews):
                    r = file_amazon_metadata.readline().strip().split(" ")
                    r = [x for x in r if x != '']  # remove ''
                    # review = {"date": r[0], "customer": r[2], "rating": r[4], "votes": r[6], "helpful": r[8]}
                    review = OrderedDict([("date", r[0]), ("customer", r[2]), ("rating", float(r[4])), ("votes", int(r[6])), ("helpful", int(r[8]))])
                    rlist.append(review)
            reviews.append(rlist)

    numOfProducts = len(ASINs)
    products = []
    for i in range(numOfProducts):
        products.append(OrderedDict([("Id", Ids[i]), ("ASIN", ASINs[i]), ("title", titles[i]), ("group", groups[i]), ("salesrank", salesranks[i]), ("avg_rating", avg_ratings[i]), ("reviews", reviews[i])]))

    with open("./datasets/amazon-products.json", "w") as f:
        json.dump(products, f)

    with open("./datasets/amazon-products.json", "rb") as f_in:
        with gzip.open("./datasets/amazon-products.json.gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    # https://pythonadventures.wordpress.com/2015/01/07/opening-gzipped-json-files/
    with gzip.open("./datasets/amazon-products.json.gz", "rb") as f:
        products = json.loads(f.read().decode("ascii"))
        print products[2]

    os.remove("./datasets/amazon-products.json")

    print "Finish preprocessing the amazon product metadata to a json file."
