import * as React from 'react';
import createHistory from 'history/createBrowserHistory'
import {Route} from 'react-router'
import {Provider} from 'react-redux';
import {render} from 'react-dom';
import {ConnectedRouter, routerMiddleware} from 'react-router-redux';
import {AppContainer} from 'react-hot-loader';
import {configureStore} from './store/configureStore';
import {RootState} from './reducers';

import {App} from './containers/App';

const initialState: RootState = {};

const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));

render(
    <AppContainer>
        <Provider store={store}>
            <ConnectedRouter history={history}>
                <div>
                    <App>
                        Rendered
                    </App>
                </div>
            </ConnectedRouter>
        </Provider>
    </AppContainer>,
    document.getElementById('root')
)

// if (module.hot) {
//     module.hot.accept('./containers/App', () => { render(App) });
// }