import { UPDATE_EXPERIMENTAL_RESULTS } from '../actions/type';

export default function(state={}, action) {
  // Attention!!! The state object here refers to state.results, instead of the application state.

  switch(action.type) {
    case UPDATE_EXPERIMENTAL_RESULTS:
      return action.payload;
    default:
      return state;
  }
}