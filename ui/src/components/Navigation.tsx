import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {Menu} from "semantic-ui-react";

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

export const UnconnectedNavigation: React.StatelessComponent<INavigationProps> = ({ isLoggedIn, login, logout }: INavigationProps & IReduxStateProps & IReduxDispatchProps) => (
    <Menu>
        <Menu.Item header>CMDMNT</Menu.Item>
        <MenuItemLink to="/devices">Devices</MenuItemLink>
        <MenuItemLink to="/profiles">Profiles</MenuItemLink>
        <MenuItemLink to="/applications">Applications</MenuItemLink>
        <MenuItemLink to="/settings">Settings</MenuItemLink>
        <MenuItemLink to="/device_groups">Groups</MenuItemLink>

    <Menu.Menu position="right">

        <Menu.Item name="logout" icon="user" onClick={logout} />

        <Menu.Item name="login" icon="user" onClick={login} />

    </Menu.Menu>
    </Menu>
);

export const Navigation = connect()(UnconnectedNavigation);
