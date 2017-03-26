import * as React from 'react';
import { connect } from 'react-redux';
import {RouteComponentProps} from 'react-router';

import {Navigation} from './Navigation';

interface AppState {

}

interface AppDispatchProps {
    
}

interface AppProps {
    
}

@connect<AppState, AppDispatchProps, RouteComponentProps>()
export class App extends React.Component<AppProps & RouteComponentProps<{}>, AppState> {

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