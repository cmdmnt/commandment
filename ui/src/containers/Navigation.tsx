import * as React from 'react';
import {Menu} from 'semantic-ui-react';
import {Link, NavLink} from 'react-router-dom';

import './Navigation.scss';
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";

export class Navigation extends React.Component<undefined, undefined> {
    render() {

        return (
            <Menu>
                <Menu.Item header>CMDMNT</Menu.Item>
                <MenuItemLink to='/devices'>Devices</MenuItemLink>
                <MenuItemLink to='/profiles'>Profiles</MenuItemLink>
                <MenuItemLink to='/settings'>Settings</MenuItemLink>
            </Menu>
        )
    }
}