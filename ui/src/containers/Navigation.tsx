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
                        <NavItem>Config</NavItem>
                    </Nav>
                    <Nav pullRight>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}