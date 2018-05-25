import { UPDATE_EXPERIMENTAL_PARAMETERS } from '../actions/type';

export default function(state={}, action) {
  switch(action.type) {
    case UPDATE_EXPERIMENTAL_PARAMETERS:
      return action.payload;
    default:
      return state;
  }
}