import * as React from 'react';
import createHistory from 'history/createBrowserHistory'
import { Route } from 'react-router'
import {Provider} from 'react-redux';
import {render} from 'react-dom';
import { ConnectedRouter, routerReducer, routerMiddleware, push } from 'react-router-redux';
import {configureStore} from './store/configureStore';

import {App} from './containers/App';

const initialState = {};


const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));


render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <div>
                <Route exact path="/" component={App} />
            </div>
        </ConnectedRouter>
    </Provider>,
    document.getElementById('root')
)
