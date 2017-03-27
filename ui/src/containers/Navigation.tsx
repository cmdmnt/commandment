import * as React from 'react';
import {Link} from 'react-router-dom';

import './Navigation.scss';

export class Navigation extends React.Component<undefined, undefined> {
    render() {

        return (
            <div className='navigation'>
                <div>CMDMNT</div>
                <div className='navitem'><Link to='/config/scep'>SCEP</Link></div>
            </div>
        )
    }
}