import { STATUS_CODE_ONE, STATUS_CODE_TWO, STATUS_CODE_THREE } from '../actions/type';

/**
 * Status Codes:
 * 0 (default): Welcome! Please run experiment to see results.
 * 1: The experiment is running. This may take couple of seconds (Disable form of parameters).
 * 2: The experimental results are shown below. You can give ratings to the experimental results.
 * 3: You have submitted your ratings. Now you can run another experiment.
 */

export default function(state={ code: 0 }, action) {

  switch(action.type) {
    case STATUS_CODE_ONE:
      return { ...state, code: 1 };
    case STATUS_CODE_TWO:
      return { ...state, code: 2 };
    case STATUS_CODE_THREE:
      return { ...state, code: 3 };
    default:
      return state;
  }
}