import createHistory from "history/createBrowserHistory";
import * as React from "react";
import {render} from "react-dom";
import {AppContainer} from "react-hot-loader";
import {Provider} from "react-redux";
import {Route} from "react-router";
import {ConnectedRouter, routerMiddleware} from "react-router-redux";
import {OidcProvider} from "redux-oidc";
import {IRootState} from "./reducers";
import {configureStore} from "./store/configureStore";

import {App} from "./containers/App";
import {SCEPPage} from "./containers/config/SCEPPage";

import {CertificatesPage} from "./containers/CertificatesPage";
import {OrganizationPage} from "./containers/config/OrganizationPage";
import {VPPPage} from "./containers/config/VPPPage";
import {DeviceGroupPage} from "./containers/DeviceGroupPage";
import {DeviceGroupsPage} from "./containers/DeviceGroupsPage";
import {DevicePage} from "./containers/DevicePage";
import {DevicesPage} from "./containers/DevicesPage";
import {ProfilePage} from "./containers/ProfilePage";
import {ProfilesPage} from "./containers/ProfilesPage";
import {SettingsPage} from "./containers/SettingsPage";

import "../sass/app.scss";
import {ApplicationPage} from "./containers/ApplicationPage";
import {ApplicationsPage} from "./containers/ApplicationsPage";
import {userManager} from "./reducers/oidc";
import {OIDCCallbackPage} from "./containers/sso/OIDCCallbackPage";

const initialState: IRootState = {};

const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <OidcProvider userManager={userManager} store={store}>
        <ConnectedRouter history={history}>
            <AppContainer>
                <App>
                    <Route path={`${window.location.protocol}//${window.location.hostname}:${window.location.port}/sso/oidc/callback`} component={OIDCCallbackPage} />

                    <Route exact path="/applications" component={ApplicationsPage} />
                    <Route path="/applications/add" component={ApplicationPage} />
                    <Route path="/certificates" component={CertificatesPage} />
                    <Route exact path="/devices" component={DevicesPage} />
                    <Route path="/devices/:id" component={DevicePage} />

                    <Route exact path="/device_groups" component={DeviceGroupsPage} />
                    <Route path="/device_groups/add" component={DeviceGroupPage} />
                    <Route path="/device_groups/:id" component={DeviceGroupPage} />

                    <Route exact path="/profiles" component={ProfilesPage} />
                    <Route path="/profiles/:id" component={ProfilePage} />

                    <Route exact path="/settings" component={SettingsPage} />
                    <Route path="/settings/scep" component={SCEPPage} />
                    <Route path="/settings/organization" component={OrganizationPage} />
                    <Route path="/settings/vpp" component={VPPPage} />
                </App>
            </AppContainer>
        </ConnectedRouter>
        </OidcProvider>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
