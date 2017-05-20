import * as React from 'react';
import {Menu} from 'semantic-ui-react';
import {Link, NavLink} from 'react-router-dom';

import './Navigation.scss';

export class Navigation extends React.Component<undefined, undefined> {
    render() {

        return (
            <Menu>
                <Menu.Item header>CMDMNT</Menu.Item>
                <Menu.Item><NavLink to='/devices'>Devices</NavLink></Menu.Item>
                <Menu.Item><NavLink to='/profiles'>Profiles</NavLink></Menu.Item>
                <Menu.Item>Settings</Menu.Item>
            </Menu>
        )
    }
}