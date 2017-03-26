import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';

import {Navigation} from './Navigation';

interface AppState {

}

interface AppDispatchProps {
    
}

interface AppProps {
    
}

@connect<AppState, AppDispatchProps, RouteComponentProps<any>>(
    state => {},
    (dispatch: Dispatch<any>) => {}
)
export class App extends React.Component<AppProps & RouteComponentProps<any>, AppState> {
    
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