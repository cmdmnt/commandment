import createHistory from "history/createBrowserHistory";
import * as React from "react";
import {render} from "react-dom";
// import {hot} from "react-hot-loader";
import {Provider} from "react-redux";
import {Route} from "react-router";
import {ConnectedRouter, routerMiddleware} from "react-router-redux";
import {RootState} from "./reducers";
import {configureStore} from "./store/configureStore";

import {AppLayout} from "./containers/AppLayout";
import {DeviceAuthPage} from "./containers/config/DeviceAuthPage";

// Settings
import {SettingsPage} from "./containers/SettingsPage";
import {CertificatesPage} from "./containers/CertificatesPage";
import {OrganizationPage} from "./containers/config/OrganizationPage";
import {VPPAccountsPage} from "./containers/settings/VPPAccountsPage";
import {DEPAccountsPage} from "./containers/settings/DEPAccountsPage";
import {APNSPage} from "./containers/settings/APNSPage";

import {DevicePage} from "./containers/DevicePage";
import {DevicesPage} from "./containers/DevicesPage";
import {ProfilePage} from "./containers/ProfilePage";
import {ProfilesPage} from "./containers/ProfilesPage";


import "../sass/app.scss";
import {ApplicationPage} from "./containers/ApplicationPage";
import {ApplicationsPage} from "./containers/ApplicationsPage";
import {DashboardPage} from "./containers/DashboardPage";
import {DEPAccountSetupPage} from "./containers/settings/DEPAccountSetupPage";
import {DEPAccountPage} from "./containers/DEPAccountPage";

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
                <Route path="/settings/vpp" component={VPPAccountsPage} />
                <Route exact path="/settings/dep/accounts" component={DEPAccountsPage} />
                <Route path="/settings/dep/accounts/add" component={DEPAccountSetupPage} />
                <Route path="/dep/accounts/:id" component={DEPAccountPage} />
            </AppLayout>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
