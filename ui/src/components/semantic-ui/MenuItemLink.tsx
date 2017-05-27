import * as React from 'react';
import {Route, Link} from 'react-router-dom';
import { Menu } from 'semantic-ui-react';

interface MenuItemLinkProps {
    to: string;
    activeOnlyWhenExact?: boolean;
}

export const MenuItemLink = ({ to, children, activeOnlyWhenExact = true }: MenuItemLinkProps) => (
    <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => (
        <Menu.Item as={Link} to={to} active={match}>{children}</Menu.Item>
    )}/>
);