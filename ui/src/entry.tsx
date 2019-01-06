import createHistory from "history/createBrowserHistory";
import * as React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import {Route} from "react-router";

import {RootState} from "./reducers";
import {configureStore, history} from "./store/configureStore";

import {AppLayout} from "./components/AppLayout";

import {ApplicationPage} from "./containers/ApplicationPage";
import {ApplicationsPage} from "./containers/ApplicationsPage";
import {DeviceAuthPage} from "./containers/config/DeviceAuthPage";
import {OrganizationPage} from "./containers/config/OrganizationPage";
import {DashboardPage} from "./containers/DashboardPage";
import {DEPAccountPage} from "./containers/DEPAccountPage";
import {DEPProfilePage} from "./containers/DEPProfilePage";
import {DevicePage} from "./containers/DevicePage";
import {DevicesPage} from "./containers/DevicesPage";
import {ProfilePage} from "./containers/ProfilePage";
import {ProfilesPage} from "./containers/ProfilesPage";
import {APNSPage} from "./containers/settings/APNSPage";
import {DEPAccountSetupPage} from "./containers/settings/DEPAccountSetupPage";
import {DEPAccountsPage} from "./containers/settings/DEPAccountsPage";
import {VPPAccountsPage} from "./containers/settings/VPPAccountsPage";
import {SettingsPage} from "./containers/SettingsPage";
import {AppStorePage} from "./containers/AppStorePage";

import "../sass/app.scss";
import {ProfileUpload} from "./containers/ProfileUpload";

const initialState: RootState = {};

import { ConnectedRouter, routerMiddleware } from "connected-react-router";

const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <AppLayout>
                <Route exact path="/" component={DashboardPage} />
                <Route exact path="/applications" component={ApplicationsPage} />
                <Route path="/applications/add/macos" component={ApplicationPage} />
                <Route path="/applications/add/mas" component={AppStorePage} />

                <Route exact path="/devices" component={DevicesPage} />
                <Route path="/devices/:id" component={DevicePage} />

                <Route exact path="/profiles" component={ProfilesPage} />
                <Route path="/profiles/add/custom" component={ProfileUpload} />
                <Route path="/profiles/id/:id" component={ProfilePage} />

                <Route exact path="/settings" component={SettingsPage} />
                <Route path="/settings/apns" component={APNSPage} />
                <Route path="/settings/deviceauth" component={DeviceAuthPage} />
                <Route path="/settings/organization" component={OrganizationPage} />
                <Route path="/settings/vpp" component={VPPAccountsPage} />
                <Route exact path="/settings/dep/accounts" component={DEPAccountsPage} />
                <Route path="/settings/dep/accounts/add" component={DEPAccountSetupPage} />
                <Route exact path="/dep/accounts/:id" component={DEPAccountPage} />
                <Route exact path="/dep/accounts/:account_id/add/profile" component={DEPProfilePage} />
                <Route exact path="/dep/accounts/:account_id/profiles/:id" component={DEPProfilePage} />
            </AppLayout>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
