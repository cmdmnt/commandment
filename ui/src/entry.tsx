import * as React from 'react';
import createHistory from 'history/createBrowserHistory'
import {Route} from 'react-router'
import {Provider} from 'react-redux';
import {render} from 'react-dom';
import {ConnectedRouter, routerMiddleware} from 'react-router-redux';
import {AppContainer} from 'react-hot-loader';
import {configureStore} from './store/configureStore';
import {IRootState} from './reducers';

import {App} from './containers/App';
import {SCEPPage} from './containers/config/SCEPPage';

import {CertificatesPage} from './containers/CertificatesPage';
import {OrganizationPage} from './containers/config/OrganizationPage';
import {DevicesPage} from "./containers/DevicesPage";
import {DevicePage} from "./containers/DevicePage";
import {ProfilesPage} from './containers/ProfilesPage';
import {SettingsPage} from './containers/SettingsPage';
import {DeviceGroupsPage} from "./containers/DeviceGroupsPage";
import {DeviceGroupPage} from "./containers/DeviceGroupPage";
import {ProfilePage} from "./containers/ProfilePage";
import {VPPPage} from "./containers/config/VPPPage";

import '../sass/app.scss';
import {ApplicationsPage} from "./containers/ApplicationsPage";
import {ApplicationPage} from "./containers/ApplicationPage";

const initialState: IRootState = {};


const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <AppContainer>
                <App>
                    <Route exact path='/applications' component={ApplicationsPage} />
                    <Route path='/applications/add' component={ApplicationPage} />
                    <Route path='/certificates' component={CertificatesPage} />
                    <Route exact path='/devices' component={DevicesPage} />
                    <Route path='/devices/:id' component={DevicePage} />

                    <Route exact path='/device_groups' component={DeviceGroupsPage} />
                    <Route path='/device_groups/add' component={DeviceGroupPage} />
                    <Route path='/device_groups/:id' component={DeviceGroupPage} />

                    <Route exact path='/profiles' component={ProfilesPage} />
                    <Route path='/profiles/:id' component={ProfilePage} />

                    <Route exact path='/settings' component={SettingsPage} />
                    <Route path='/settings/scep' component={SCEPPage} />
                    <Route path='/settings/organization' component={OrganizationPage} />
                    <Route path='/settings/vpp' component={VPPPage} />
                </App>
            </AppContainer>
        </ConnectedRouter>
    </Provider>,
    document.getElementById('root') as HTMLElement
);

