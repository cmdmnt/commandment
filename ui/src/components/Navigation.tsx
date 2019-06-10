import * as React from "react";
import {Menu} from "semantic-ui-react";

import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import "./Navigation.scss";

export interface INavigationProps {

}

export const Navigation: React.StatelessComponent<INavigationProps> = (props: INavigationProps) => (
    <Menu>
        <MenuItemLink header to="/" activeOnlyWhenExact>CMDMNT</MenuItemLink>
        <MenuItemLink to="/devices">Devices</MenuItemLink>
        <MenuItemLink to="/profiles">Profiles</MenuItemLink>
        <MenuItemLink to="/applications">Applications</MenuItemLink>
        <MenuItemLink to="/settings">Settings</MenuItemLink>
    </Menu>
);
