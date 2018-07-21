import createHistory from "history/createBrowserHistory";
import * as React from "react";
import {render} from "react-dom";
import {hot} from "react-hot-loader";
import {Provider} from "react-redux";
import {Route} from "react-router";
import {ConnectedRouter, routerMiddleware} from "react-router-redux";
import {RootState} from "./reducers";
import {configureStore} from "./store/configureStore";

import {AppLayout} from "./containers/AppLayout";
import {DeviceAuthPage} from "./containers/config/DeviceAuthPage";

import {CertificatesPage} from "./containers/CertificatesPage";
import {OrganizationPage} from "./containers/config/OrganizationPage";
import {VPPPage} from "./containers/config/VPPPage";
import {DEPAccountsPage} from "./containers/settings/DEPAccountsPage";
import {DevicePage} from "./containers/DevicePage";
import {DevicesPage} from "./containers/DevicesPage";
import {ProfilePage} from "./containers/ProfilePage";
import {ProfilesPage} from "./containers/ProfilesPage";
import {SettingsPage} from "./containers/SettingsPage";

import "../sass/app.scss";
import {ApplicationPage} from "./containers/ApplicationPage";
import {ApplicationsPage} from "./containers/ApplicationsPage";
import {DashboardPage} from "./containers/DashboardPage";
import {APNSPage} from "./containers/config/APNSPage";

const initialState: RootState = {};

const history = createHistory();
const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <AppLayout>
                <Route exact path="/" component={DashboardPage} />
                <Route exact path="/applications" component={ApplicationsPage} />
                <Route path="/applications/add/:platform" component={ApplicationPage} />
                <Route path="/certificates" component={CertificatesPage} />
                <Route exact path="/devices" component={DevicesPage} />
                <Route path="/devices/:id" component={DevicePage} />

                <Route exact path="/profiles" component={ProfilesPage} />
                <Route path="/profiles/:id" component={ProfilePage} />

                <Route exact path="/settings" component={SettingsPage} />
                <Route path="/settings/apns" component={APNSPage} />
                <Route path="/settings/deviceauth" component={DeviceAuthPage} />
                <Route path="/settings/organization" component={OrganizationPage} />
                <Route path="/settings/vpp" component={VPPPage} />
                <Route path="/settings/dep" component={DEPAccountsPage} />
            </AppLayout>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
