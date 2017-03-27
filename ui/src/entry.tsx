import * as React from 'react';
import createHistory from 'history/createBrowserHistory'
// import {Route} from 'react-router'
import {Provider} from 'react-redux';
import {render} from 'react-dom';
import {ConnectedRouter, routerMiddleware} from 'react-router-redux';
import {AppContainer} from 'react-hot-loader';
import {configureStore} from './store/configureStore';
import {RootState} from './reducers';

import {App} from './containers/App';
import '../sass/app.scss';

const initialState: RootState = {};


const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));



render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <AppContainer>
                <App>
                    Rendered
                </App>
            </AppContainer>
        </ConnectedRouter>
    </Provider>,
    document.getElementById('root')
)
