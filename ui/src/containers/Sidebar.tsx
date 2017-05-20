import * as React from 'react';
import { Sidebar, Segment, Button, Menu, Image, Icon, Header } from 'semantic-ui-react';
import { NavLink } from 'react-router-dom';

export class Sidebar extends React.Component<any, any> {
    state = { visible: false };

    render() {
        const {
            children
        } = this.props;

        return (
            <div>
                <Sidebar.Pushable>
                    <Sidebar as={Menu} animation='push' width='thin' visible={true} icon='labeled' vertical inverted>
                        <NavLink to="/devices">
                            <Menu.Item name='devices'>
                                <Icon name='mobile' />
                                Devices
                            </Menu.Item>
                        </NavLink>
                        <NavLink to="/profiles">
                            <Menu.Item name='profiles'>
                                <Icon name='setting' />
                                Profiles
                            </Menu.Item>
                        </NavLink>
                        <Menu.Item name='configure'>
                            <Icon name='options' />
                            Configure
                        </Menu.Item>
                    </Sidebar>
                    <Sidebar.Pusher>
                        {children}
                    </Sidebar.Pusher>
                </Sidebar.Pushable>
            </div>
        )
    }
}