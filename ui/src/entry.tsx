import createHistory from "history/createBrowserHistory";
import * as React from "react";
import {render} from "react-dom";
import {Provider} from "react-redux";
import {Route} from "react-router";

import {RootState} from "./reducers";
import {configureStore, history} from "./store/configureStore";

import {App} from "./components/App";

import {ApplicationPage} from "./containers/ApplicationPage";
import {MacOSEntApplicationPage} from "./containers/applications/MacOSEntApplicationPage";
import {ApplicationsPage} from "./containers/ApplicationsPage";
import {AppStorePage} from "./containers/AppStorePage";
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
import {LoginPage} from "./containers/LoginPage";

import "../sass/app.scss";
import {ProfileUpload} from "./containers/ProfileUpload";

const initialState: RootState = {};

import { ConnectedRouter, routerMiddleware } from "connected-react-router";
import {NavigationLayout} from "./components/NavigationLayout";
import {BareLayout} from "./components/BareLayout";
import {ProtectedRoute} from "./components/ProtectedRoute";

const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <BareLayout exact path="/login" component={LoginPage} />
            <App>
                <NavigationLayout>
                    <ProtectedRoute exact path="/" component={DashboardPage} />
                    <ProtectedRoute exact path="/applications" component={ApplicationsPage} />
                    <ProtectedRoute path="/applications/id/:id" component={ApplicationPage} />
                    <ProtectedRoute path="/applications/add/macos" component={MacOSEntApplicationPage} />
                    <ProtectedRoute path="/applications/add/:entity" component={AppStorePage} />
                    <ProtectedRoute exact path="/devices" component={DevicesPage} />
                    <ProtectedRoute path="/devices/:id" component={DevicePage} />
                    <ProtectedRoute exact path="/profiles" component={ProfilesPage} />
                    <ProtectedRoute path="/profiles/add/custom" component={ProfileUpload} />
                    <ProtectedRoute path="/profiles/id/:id" component={ProfilePage} />
                    <ProtectedRoute exact path="/settings" component={SettingsPage} />
                    <ProtectedRoute path="/settings/apns" component={APNSPage} />
                    <ProtectedRoute path="/settings/deviceauth" component={DeviceAuthPage} />
                    <ProtectedRoute path="/settings/organization" component={OrganizationPage} />
                    <ProtectedRoute path="/settings/vpp" component={VPPAccountsPage} />
                    <ProtectedRoute exact path="/settings/dep/accounts" component={DEPAccountsPage} />
                    <ProtectedRoute path="/settings/dep/accounts/add" component={DEPAccountSetupPage} />
                    <ProtectedRoute exact path="/dep/accounts/:id" component={DEPAccountPage} />
                    <ProtectedRoute exact path="/dep/accounts/:account_id/add/profile" component={DEPProfilePage} />
                    <ProtectedRoute exact path="/dep/accounts/:account_id/profiles/:id" component={DEPProfilePage} />
                </NavigationLayout>
            </App>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
