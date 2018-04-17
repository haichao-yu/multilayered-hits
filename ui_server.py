from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo

from src.load_data import load_data_multilayered_hits_ranking
from src.load_data import load_data_multilayered_hits_query
from src.load_data import load_data_regular_hits_ranking
from src.load_data import load_data_regular_hits_query

from src.multilayered_hits import multilayered_hits
from src.regular_hits import regular_hits
from src.get_experimental_results import get_experimental_results


app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'amazon'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/amazon'
mongo = PyMongo(app)
dataset = './AmazonDataProcessing/datasets/amazon-data-graph.npy'


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/api/run_experiment')
def run_experiment():

    # Get parameters
    algorithm = request.args.get('algorithm')  # if key doesn't exist, returns None
    query_node_index = request.args.get('query_node_index')  # -1 means no query node -> ranking globally
    if query_node_index is None:
        return 'Hello world!'
    query_node_index = int(query_node_index)

    layers = ('book', 'dvd', 'music', 'video')
    selected_layers = []
    for l in layers:
        if request.args.get('is_' + l + '_selected') == 'true':
            selected_layers.append(l)
    print selected_layers

    # Run experiment
    data = None
    u = None
    v = None
    if algorithm == 'regular_hits':
        if query_node_index == -1:  # 'ranking'
            data = load_data_regular_hits_ranking(dataset, selected_layers)
        else:  # 'query'
            data = load_data_regular_hits_query(dataset, selected_layers, query_node_index=query_node_index)
        A = data['adjacency_matrix']
        [u, v] = regular_hits(A)
    elif algorithm == 'multilayered_hits':
        if query_node_index == -1:  # 'ranking'
            data = load_data_multilayered_hits_ranking(dataset, selected_layers)
        else:  # 'query'
            data = load_data_multilayered_hits_query(dataset, selected_layers, query_node_index=query_node_index)
        G = data['GroupNet']
        A = data['WithinLayerNets']
        D = data['CrossLayerDependencies']
        [u, v] = multilayered_hits(G, A, D)
    experimental_results = get_experimental_results(mongo.db.products, selected_layers, data, u, v)

    return jsonify(experimental_results)


@app.route('/api/submit_ratings', methods=['POST'])
def submit_ratings():

    # Submit ratings data to 'ratings' collection
    formatted_ratings = request.get_json()['formatted_ratings']
    mongo.db.ratings.insert_many(formatted_ratings)

    return "The ratings have been submitted successfully!"


if __name__ == '__main__':
    app.run()
