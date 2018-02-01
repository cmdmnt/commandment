import * as React from "react";
import {Link, Route} from "react-router-dom";
import { Menu } from "semantic-ui-react";

interface IMenuItemLinkProps {
    to: string;
    activeOnlyWhenExact?: boolean;
    children: any;
}

export const MenuItemLink = ({ to, children, activeOnlyWhenExact = false }: IMenuItemLinkProps) => (
    <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => (
        <Menu.Item as={Link} to={to} active={!!match}>{children}</Menu.Item>
    )}/>
);
