# Multilayered HITS

Multilayered HITS is an algorithm which generalize the regular HITS algorithm to multilayered networks. This algorithm considers both *within-layer smoothness* and *cross-layer consistency*.

**Multilayered Networks** can be represented as a quintuple Γ =< G, A, D, θ, φ >, where G is a binary g × g abstract layer-layer dependency network, A = {A1, ..., Ag} is a set of within- layer adjacency matrices, D is a set of inter-layer node-node dependency matrices, θ is a one-to-one mapping function that maps each node in layer-layer dependency notwork to the corresponding within-layer adjacency matrix, φ is another one-to-one mapping function that maps each edge to the corresponding inter-layer node- node dependency matrix.

## Input
This algorithm takes a multilayered networks model as its input. *iteration_times* is parameter representing the number of multiplicative updating times. *mu* is a parameter representing the weight of cross-layer consistency compared to within-layer smoothness. 

## Output
This algorithm gives authority score and hub score for each node in each layer.

## Dataset
The dataset in this repository is a five layer Italy network in the critical infrastructure domain (INFRA-5). This dataset is provided by Ms. Chen Chen.

## Deploy
You can refer to [this link](https://progblog.io/How-to-deploy-a-Flask-App-to-Heroku/).

## Remark
This is the very first version of the code. And many optimization is need to do. For questions please contact the author by __haichaoy@asu.edu__. 
