import * as React from 'react';
import {Route, Link} from 'react-router-dom';
import { Menu } from 'semantic-ui-react';

export const MenuItemLink = ({ label, to, activeOnlyWhenExact = true }) => (
    <Route path={to} exact={activeOnlyWhenExact} children={({ match }) => (
        <Menu.Item as={Link} to={to} active={match}>{label}</Menu.Item>
    )}/>
);