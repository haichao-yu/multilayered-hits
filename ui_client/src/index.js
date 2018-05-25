import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import reduxThunk from 'redux-thunk';

import Header from './components/header';
import Introduction from "./components/introduction";
import Parameters from './components/parameters';
import Results from './components/results';

import reducers from './reducers';

const createStoreWithMiddleware = applyMiddleware(reduxThunk)(createStore);
const store = createStoreWithMiddleware(reducers);

ReactDOM.render(
  <Provider store={store}>
    <div>
      <Header />
      <div className="container" id="content">
        <Introduction />
        <Parameters />
        <Results />
      </div>
    </div>
  </Provider>
  , document.getElementById('root')
);