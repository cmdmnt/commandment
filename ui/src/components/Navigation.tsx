import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {Menu} from "semantic-ui-react";

import {bindActionCreators} from "redux";
import {login, logout} from "redux-implicit-oauth2";
import {IRootState} from "../reducers/index";
import {MenuItemLink} from "./semantic-ui/MenuItemLink";

export interface IReduxStateProps {
        isLoggedIn: boolean;
}

export interface IReduxDispatchProps {
    login: () => void;
    logout: () => void;
}

export interface INavigationProps {
}

const config = {
    url: "https://accounts.google.com/o/oauth2/v2/auth",
    client: window.OAUTH2_CLIENT_ID,
    redirect: window.OAUTH2_REDIRECT_URL,
    scope: "https://www.googleapis.com/auth/drive.metadata.readonly",
    width: 400, // Width (in pixels) of login popup window. Optional, default: 400
    height: 400, // Height (in pixels) of login popup window. Optional, default: 400
};

export const UnconnectedNavigation: React.StatelessComponent<INavigationProps> = ({ isLoggedIn, login, logout }: INavigationProps & IReduxStateProps & IReduxDispatchProps) => (
    <Menu>
        <Menu.Item header>CMDMNT</Menu.Item>
        <MenuItemLink to="/devices">Devices</MenuItemLink>
        <MenuItemLink to="/profiles">Profiles</MenuItemLink>
        <MenuItemLink to="/applications">Applications</MenuItemLink>
        <MenuItemLink to="/settings">Settings</MenuItemLink>
        <MenuItemLink to="/device_groups">Groups</MenuItemLink>

    <Menu.Menu position="right">
        {isLoggedIn &&
        <Menu.Item name="logout" icon="user" onClick={logout} />
        }
        {!isLoggedIn &&
        <Menu.Item name="login" icon="user" onClick={login} />
        }

    </Menu.Menu>
    </Menu>
);

export const Navigation = connect(
    (state: IRootState) => ({ isLoggedIn: state.auth.isLoggedIn }),
    (dispatch: Dispatch<IRootState>, ownProps?: any) => bindActionCreators({ login: () => login(config), logout }, dispatch),
)(UnconnectedNavigation);
