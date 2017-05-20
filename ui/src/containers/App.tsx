import * as React from 'react';
import { connect, Dispatch } from 'react-redux';

import {Navigation} from './Navigation';
// import {Sidebar} from './Sidebar';

@connect()
export class App extends React.Component<undefined, undefined> {
    
    render() {
        const {
            children
        } = this.props;

        return (
            <div>
                <Navigation />
                {children}
            </div>
        )
    }

}