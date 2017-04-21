import * as React from 'react';
import {Link} from 'react-router-dom';

import './Navigation.scss';

export class Navigation extends React.Component<undefined, undefined> {
    render() {

        return (
            <nav className='navigation'>
                <ul>
                    <li><span>CMDMNT</span></li>
                    <li><a href="#">Configure</a>
                        <ul>
                            <li><Link to='/config/organization'>Organization</Link></li>
                            <li><Link to='/config/scep'>SCEP</Link></li>
                        </ul>
                    </li>
                    <li><Link to='/config/assistant'>Assistant</Link></li>

                    <li><Link to='/config/ssl'>SSL</Link></li>
                    <li><Link to='/config/mdm'>MDM</Link></li>
                    <li><Link to='/certificates'>Certificates</Link></li>
                    <li><Link to='/devices'>Devices</Link></li>
                    <li><Link to='/profiles'>Profiles</Link></li>
                </ul>
            </nav>
        )
    }
}