import * as React from 'react';
import { connect } from 'react-redux';

interface AppState {

}

interface AppProps {
    
}

@connect()
export class App extends React.Component<AppProps, AppState> {

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