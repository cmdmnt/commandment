import * as React from "react";
import Menu from "semantic-ui-react/src/collections/Menu";

import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import "./Navigation.scss";
import Sidebar from "semantic-ui-react/dist/commonjs/modules/Sidebar/Sidebar";
import {RouteComponentProps} from "react-router";
import {Divider} from "semantic-ui-react";

interface IRouteProps {
}

export interface INavigationVerticalProps extends RouteComponentProps<IRouteProps> {

}

export const NavigationVertical: React.FC<INavigationVerticalProps> = (props: INavigationVerticalProps) => (
    <Sidebar as={Menu} secondary vertical visible>
            <MenuItemLink header to="/" activeOnlyWhenExact>CMDMNT</MenuItemLink>
            <MenuItemLink to="/devices">Devices</MenuItemLink>
            <MenuItemLink to="/profiles">Profiles</MenuItemLink>
            <MenuItemLink to="/applications">Applications</MenuItemLink>
            <MenuItemLink to="/settings">Settings</MenuItemLink>
            <Divider />
            <MenuItemLink to="/logout">Logout</MenuItemLink>
    </Sidebar>
);
