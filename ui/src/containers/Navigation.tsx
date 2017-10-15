import * as React from 'react';
import {Menu} from 'semantic-ui-react';

import './Navigation.scss';
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";

export const Navigation: React.StatelessComponent<void> = () => (
    <Menu>
        <Menu.Item header>CMDMNT</Menu.Item>
        <MenuItemLink to='/devices'>Devices</MenuItemLink>
        <MenuItemLink to='/profiles'>Profiles</MenuItemLink>
        <MenuItemLink to='/applications'>Applications</MenuItemLink>
        <MenuItemLink to='/settings'>Settings</MenuItemLink>
        <MenuItemLink to='/device_groups'>Groups</MenuItemLink>
    </Menu>
);
