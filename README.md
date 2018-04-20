# Multilayered HITS

Multilayered HITS is an algorithm which generalize the regular HITS algorithm to multilayered networks. This algorithm considers both *within-layer smoothness* and *cross-layer consistency*.

**Multilayered Networks** can be represented as a quintuple Γ =< G, A, D, θ, φ >, where G is a binary g × g abstract layer-layer dependency network, A = {A1, ..., Ag} is a set of within- layer adjacency matrices, D is a set of inter-layer node-node dependency matrices, θ is a one-to-one mapping function that maps each node in layer-layer dependency notwork to the corresponding within-layer adjacency matrix, φ is another one-to-one mapping function that maps each edge to the corresponding inter-layer node- node dependency matrix.

## Input
This algorithm takes a multilayered networks model as its input. *iteration_times* is parameter representing the number of multiplicative updating times. *mu* is a regularization parameter representing the weight of cross-layer consistency compared to within-layer smoothness. 

## Output
This algorithm gives authority score and hub score for each node in each layer.

## Prototype
We developed a prototype system for multi-layered HITS algorithm [[link]](http://thesis.haichaoy.com/). In this prototype, you can conduct comprehensive experiments with different parameters to evaluate the algorithm. The dataset is based on [Amazon Co-purchasing Network](http://snap.stanford.edu/data/com-Amazon.html).

This prototype provides 2 kinds of tasks: Ranking and Query. For ranking task, you need to specify the Query Node Index to -1. Then the products in each selected layers will be ranked according to its global importance. For query task, you need to provide a query node. Then the products in each selected layers will be ranked according to its relevance with the specified query node. Ranking task may take a dozen of seconds. Query task may take a couple of seconds.

Each time you run the experiment, you will get the top K ranked products for each selected layer. The first product sequence is ranked by its authority score. The second product sequence is ranked by its hub score. For more information about authority and hub, please refer to [HITS Algorithm](https://en.wikipedia.org/wiki/HITS_algorithm).

## Deployment
You can refer to [this link](https://progblog.io/How-to-deploy-a-Flask-App-to-Heroku/).

## Remark
For questions please contact the author by __haichaoy@asu.edu__.