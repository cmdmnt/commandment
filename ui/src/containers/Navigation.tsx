import * as React from 'react';
import {Link} from 'react-router';
import {connect} from 'react-redux';
import {Navbar, Nav, NavItem, MenuItem, NavDropdown} from 'react-bootstrap';

@connect()
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
                        <Link></Link>
                    </Nav>
                    <Nav pullRight>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}