import { combineReducers } from 'redux';
import { reducer as FormReducer } from 'redux-form';
import StatusReducer from './status_reducer';
import ParametersReducer from './parameters_reducer';
import ResultsReducer from './results_reducer';

const rootReducer = combineReducers({
  form: FormReducer,  // the form property of state is going to be produced by ReduxForm reducer
  status: StatusReducer,
  parameters: ParametersReducer,
  results: ResultsReducer,
});

export default rootReducer;