import * as React from "react";
import {Link, Route} from "react-router-dom";
import {Menu} from "semantic-ui-react";

interface IMenuItemLinkProps {
    to: string;
    activeOnlyWhenExact?: boolean;
    header?: boolean;
    children: any;
}

export const MenuItemLink = ({ to, children, activeOnlyWhenExact = false, header = false }: IMenuItemLinkProps) => (
    <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => (
        <Menu.Item as={Link} to={to} active={match ? true : undefined} header={header}>{children}</Menu.Item>
    )}/>
);
