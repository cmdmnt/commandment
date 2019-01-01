import * as React from "react";
import Menu from "semantic-ui-react/src/collections/Menu";

import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import "./Navigation.scss";
import Sidebar from "semantic-ui-react/dist/commonjs/modules/Sidebar/Sidebar";

export interface INavigationProps {

}

export const NavigationVertical: React.StatelessComponent<INavigationProps> = (props: INavigationProps) => (
    <Sidebar as={Menu} secondary vertical visible>
        <MenuItemLink header to="/" activeOnlyWhenExact>CMDMNT</MenuItemLink>
        <MenuItemLink to="/devices">Devices</MenuItemLink>
        <MenuItemLink to="/profiles">Profiles</MenuItemLink>
        <MenuItemLink to="/applications">Applications</MenuItemLink>
        <MenuItemLink to="/settings">Settings</MenuItemLink>
    </Sidebar>
);
