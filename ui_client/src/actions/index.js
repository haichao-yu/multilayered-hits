import axios from 'axios';
import { reset } from 'redux-form';
import {
  UPDATE_EXPERIMENTAL_PARAMETERS,
  UPDATE_EXPERIMENTAL_RESULTS,
  STATUS_CODE_ONE, STATUS_CODE_TWO, STATUS_CODE_THREE
} from './type';

const ROOT_URL = '/api';

export function updateParameters(experimentalParameters) {
  return {
    type: UPDATE_EXPERIMENTAL_PARAMETERS,
    payload: experimentalParameters,
  }
}

export function runExperiment(experimentalParameters) {
  return function(dispatch) {
    axios.get(`${ROOT_URL}/run_experiment`, {
      params: experimentalParameters
    }).then((response) => {
      // The experimental results have been returned after running
      dispatch({
        type: UPDATE_EXPERIMENTAL_RESULTS,
        payload: response.data,
      });
      // Display experimental results
      dispatch({
        type: STATUS_CODE_TWO,
      })
    });
  }
}

export function submitRatings(experimentalParameters, ratings) {

  let layers = ['book', 'dvd', 'music', 'video'];
  let selected_layers = [];
  layers.forEach(function(item) {
    if (experimentalParameters['is_'.concat(item, '_selected')] === true) {
      selected_layers.push(item);
    }
  });

  let formattedRatings = [];
  selected_layers.forEach(function(item) {
    formattedRatings.push({
      'algorithm': experimentalParameters['algorithm'],
      'query_node_index': parseInt(experimentalParameters['query_node_index'], 10),
      'is_book_selected': experimentalParameters['is_book_selected'],
      'is_dvd_selected': experimentalParameters['is_dvd_selected'],
      'is_music_selected': experimentalParameters['is_music_selected'],
      'is_video_selected': experimentalParameters['is_video_selected'],
      'is_customer_selected': experimentalParameters['is_customer_selected'],
      'ranking_metric': 'authority',
      'group': item,
      'rating': parseFloat(ratings['rating_'.concat(item, '_authority')]),
    });
    formattedRatings.push({
      'algorithm': experimentalParameters['algorithm'],
      'query_node_index': parseInt(experimentalParameters['query_node_index'], 10),
      'is_book_selected': experimentalParameters['is_book_selected'],
      'is_dvd_selected': experimentalParameters['is_dvd_selected'],
      'is_music_selected': experimentalParameters['is_music_selected'],
      'is_video_selected': experimentalParameters['is_video_selected'],
      'is_customer_selected': experimentalParameters['is_customer_selected'],
      'ranking_metric': 'hub',
      'group': item,
      'rating': parseFloat(ratings['rating_'.concat(item, '_hub')]),
    });
  });

  return function(dispatch) {
    axios.post(`${ROOT_URL}/submit_ratings`, { 'formatted_ratings': formattedRatings })
      .then(() => {
        dispatch(reset('ratings'));  // Clear the form if success
        dispatch({
          type: STATUS_CODE_THREE,
        })
      })
      .catch(() => {
        // Exception Handler
      });
  };
}

// Experiment Running
export function toStatusCodeOne() {
  return { type: STATUS_CODE_ONE };
}