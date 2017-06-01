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
import {AssistantPage} from './containers/config/AssistantPage';
import {SCEPPage} from './containers/config/SCEPPage';
import '../sass/app.scss';
import {SSLPage} from "./containers/config/SSLPage";
import {CertificatesPage} from './containers/CertificatesPage';
import {InternalCAPage} from './containers/config/InternalCAPage';
import {OrganizationPage} from './containers/config/OrganizationPage';
import {DevicesPage} from "./containers/DevicesPage";
import {DevicePage} from "./containers/DevicePage";
import {ProfilesPage} from './containers/ProfilesPage';
import {SettingsPage} from './containers/SettingsPage';
import {DeviceGroupsPage} from "./containers/DeviceGroupsPage";
import {DeviceGroupPage} from "./containers/DeviceGroupPage";

const initialState: RootState = {};


const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <AppContainer>
                <App>
                    <Route path='/config/assistant' component={AssistantPage} />

                    <Route path='/config/ca' component={InternalCAPage} />
                    <Route path='/config/ssl' component={SSLPage} />

                    <Route path='/certificates' component={CertificatesPage} />
                    <Route path='/devices' exact component={DevicesPage} />
                    <Route path='/devices/:id' component={DevicePage} />
                    <Route path='/device_groups' exact component={DeviceGroupsPage} />
                    <Route path='/device_groups/add' component={DeviceGroupPage} />
                    <Route path='/profiles' component={ProfilesPage} />
                    <Route exact path='/settings' component={SettingsPage} />
                    <Route path='/settings/scep' component={SCEPPage} />
                    <Route path='/settings/organization' component={OrganizationPage} />
                </App>
            </AppContainer>
        </ConnectedRouter>
    </Provider>,
    document.getElementById('root')
);

