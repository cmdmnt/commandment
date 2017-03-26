import * as React from 'react';
import {Link} from 'react-router-dom';
import {Navbar, Nav, NavItem, MenuItem, NavDropdown} from 'react-bootstrap';

export class Navigation extends React.Component<undefined, undefined> {
    render() {

        return (
            <Navbar inverse>
                <Navbar.Header>
                    <Navbar.Brand>
                        CMDMNT
                    </Navbar.Brand>
                    <Navbar.Toggle />
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav>
                        <li><Link to='/devices'>Devices</Link></li>
                        <li><Link to='/groups'>Groups</Link></li>
                        <li><Link to='/profiles'>Profiles</Link></li>
                        <li><Link to='/apps'>Apps</Link></li>
                        <li><Link to='/dep'>DEP</Link></li>
                        <li><Link to='/certificates'>Certs</Link></li>
                        <li><Link to='/config'>Config</Link></li>
                    </Nav>
                    <Nav pullRight>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}