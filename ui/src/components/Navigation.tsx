import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {Menu} from "semantic-ui-react";

import {MenuItemLink} from "./semantic-ui/MenuItemLink";
import {login, logout} from "redux-implicit-oauth2";
import {IRootState} from "../reducers/index";
import {bindActionCreators} from "redux";

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
    client: "18556572230-jbj8kqk6rivl5thble54ed0ioc3f65au.apps.googleusercontent.com",
    redirect: "https://commandment.dev:5443/oauth/authorize",
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
