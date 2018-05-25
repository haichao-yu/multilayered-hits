import React, { Component } from 'react';

export default class Introduction extends Component {
  render() {
    return (
      <div className="mt-3">
        <h1>Introduction</h1>
        <p className="text-justify">
          This is a prototype system of multi-layered HITS algorithm.
          In this prototype, you can conduct comprehensive experiments with different parameters to evaluate the algorithm.
          The dataset is based on <a href="http://snap.stanford.edu/data/com-Amazon.html" target="_blank" rel="noopener noreferrer">Amazon Co-purchasing Network</a>.
          For more information about our work, please refer to <a href="https://github.com/haichao-yu/MultilayeredHITS" target="_blank" rel="noopener noreferrer">here</a>.
        </p>
        <p className="text-justify">
          This prototype provides 2 kinds of tasks: <b>Ranking</b> and <b>Query</b>.
          For ranking task, you need to specify the Query Node Index to -1. Then the products in each selected layers will be ranked according to its global importance (popularity).
          For query task, you need to provide a query node. Then the products in each selected layers will be ranked according to its relevance w.r.t. the specified query node.
        </p>
        <p className="text-justify">
          Each time you run the experiment, you will get the <b>top K ranked products</b> for each selected layer.
          The first product sequence is ranked by its <u>authority</u> score. The second product sequence is ranked by its <u>hub</u> score.
          For more information about authority and hub, please refer to <a href="https://en.wikipedia.org/wiki/HITS_algorithm" target="blank">HITS Algorithm</a>.
        </p>
        <h4>Temporary Notice About Human Evaluation:</h4>
        <p className="text-justify">
          Hello, thank you so much for the support. For now, we have designed 8 experiments.
          Please follow the instructions and give your evaluation regarding the relevance of the ranking sequence.
        </p>

        <p><b>Experiment 1: Ranking - Regular HITS (Single Layer)</b></p>
        <ol>
          <li>Select regular HITS algorithm;</li>
          <li>Specify the query node index to -1;</li>
          <li>Check only Book layer;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 2: Ranking - Regular HITS</b></p>
        <ol>
          <li>Select regular HITS algorithm;</li>
          <li>Specify the query node index to -1;</li>
          <li>Check layers of Book, DVD, Music, Video;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 3: Ranking - Multi-layered HITS</b></p>
        <ol>
          <li>Select multi-layered HITS algorithm;</li>
          <li>Specify the query node index to -1;</li>
          <li>Check layers of Book, DVD, Music, Video;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 4: Ranking - Multi-layered HITS (With Customer)</b></p>
        <ol>
          <li>Select multi-layered HITS algorithm;</li>
          <li>Specify the query node index to -1;</li>
          <li>Check layers of Book, DVD, Music, Video, Customer;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 5: Query - Regular HITS (Single Layer)</b></p>
        <ol>
          <li>Select regular HITS algorithm;</li>
          <li>Specify the query node index to 27705, 51900, 203495, 253670, 318220, 327317 one by one;</li>
          <li>Check only Book layer;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 6: Query - Regular HITS</b></p>
        <ol>
          <li>Select regular HITS algorithm;</li>
          <li>Specify the query node index to 27705, 51900, 203495, 253670, 318220, 327317 one by one;</li>
          <li>Check layers of Book, DVD, Music, Video;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 7: Query - Multi-layered HITS</b></p>
        <ol>
          <li>Select multi-layered HITS algorithm;</li>
          <li>Specify the query node index to 27705, 51900, 203495, 253670, 318220, 327317 one by one;</li>
          <li>Check layers of Book, DVD, Music, Video;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>

        <p><b>Experiment 8: Query - Multi-layered HITS (With Customer)</b></p>
        <ol>
          <li>Select multi-layered HITS algorithm;</li>
          <li>Specify the query node index to 27705, 51900, 203495, 253670, 318220, 327317 one by one;</li>
          <li>Check layers of Book, DVD, Music, Video, Customer;</li>
          <li>Run experiment and submit your ratings.</li>
        </ol>
      </div>
    );
  }
}