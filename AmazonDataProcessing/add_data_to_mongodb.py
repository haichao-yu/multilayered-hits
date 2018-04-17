import gzip
import json
from pymongo import MongoClient


def add_data_to_mongodb():

    DATABASE_NAME = "amazon"
    COLLECTION_NAME = "products"
    JSON_PRODUCTS = "./datasets/amazon-products.json.gz"

    # Getting Connection from MongoDB
    conn = MongoClient('mongodb://localhost:27017/')

    # Creating a DB named "amazon" in MongoDB if it doesn't exist
    print "Creating database named as " + DATABASE_NAME + " if it doesn't exist"
    database = conn[DATABASE_NAME]

    # Creating a collection named "products" if it doesn't exist
    print "Creating a collection in " + DATABASE_NAME + " named as " + COLLECTION_NAME + " if it doesn't exist"
    products = database[COLLECTION_NAME]

    # Loading products data from a json file to MongoDB if the collection is empty
    print "Loading " + JSON_PRODUCTS + " to the collection " + COLLECTION_NAME + " if it is empty"
    if products.count() == 0:
        try:
            with gzip.open(JSON_PRODUCTS) as f:
                products.insert_many(json.loads(f.read().decode("ascii")))
        except Exception as e:
            print "Error: " + str(e)

    return products


"""
Command for importing json data to MongoDB:
mongoimport -h hostname -d dbname -c collectionname -u dbuser -p dbpassword --file filename.json --jsonArray
"""
