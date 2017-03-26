import * as React from 'react';
import { connect } from 'react-redux';
import {RouteComponentProps} from 'react-router';

interface AppState {

}

interface AppProps {
    
}

@connect()
export class App extends React.Component<AppProps & RouteComponentProps<{}>, AppState> {

    render() {
        const {
            children
        } = this.props;

        return (
            <div>
                {children}
            </div>
        )
    }

}