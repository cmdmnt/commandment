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

const store = configureStore(initialState, routerMiddleware(history));

render(
    <Provider store={store}>
        <ConnectedRouter history={history}>
            <App>
                <BareLayout exact path="/login" component={LoginPage} />

                <NavigationLayout exact path="/" component={DashboardPage} />
                <NavigationLayout exact path="/applications" component={ApplicationsPage} />
                <NavigationLayout path="/applications/id/:id" component={ApplicationPage} />
                <NavigationLayout path="/applications/add/macos" component={MacOSEntApplicationPage} />
                <NavigationLayout path="/applications/add/:entity" component={AppStorePage} />

                <NavigationLayout exact path="/devices" component={DevicesPage} />
                <NavigationLayout path="/devices/:id" component={DevicePage} />

                <NavigationLayout exact path="/profiles" component={ProfilesPage} />
                <NavigationLayout path="/profiles/add/custom" component={ProfileUpload} />
                <NavigationLayout path="/profiles/id/:id" component={ProfilePage} />

                <NavigationLayout exact path="/settings" component={SettingsPage} />
                <NavigationLayout path="/settings/apns" component={APNSPage} />
                <NavigationLayout path="/settings/deviceauth" component={DeviceAuthPage} />
                <NavigationLayout path="/settings/organization" component={OrganizationPage} />
                <NavigationLayout path="/settings/vpp" component={VPPAccountsPage} />
                <NavigationLayout exact path="/settings/dep/accounts" component={DEPAccountsPage} />
                <NavigationLayout path="/settings/dep/accounts/add" component={DEPAccountSetupPage} />
                <NavigationLayout exact path="/dep/accounts/:id" component={DEPAccountPage} />
                <NavigationLayout exact path="/dep/accounts/:account_id/add/profile" component={DEPProfilePage} />
                <NavigationLayout exact path="/dep/accounts/:account_id/profiles/:id" component={DEPProfilePage} />
            </App>
        </ConnectedRouter>
    </Provider>,
    document.getElementById("root") as HTMLElement,
);
