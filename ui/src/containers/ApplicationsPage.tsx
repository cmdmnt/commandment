import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {RouteComponentProps} from "react-router";
import {RootState} from "../reducers/index";
import {bindActionCreators} from "redux";

interface ReduxStateProps {

}

interface ReduxDispatchProps {

}


interface ApplicationsPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {

}

interface ApplicationsPageState {
}

class UnconnectedApplicationsPage extends React.Component<ApplicationsPageProps, ApplicationsPageState> {
    render() {
        return (
            <div className='ApplicationsPage top-margin container'>
                <div className='row'>
                    <div className='column'>
                        <h1>Applications</h1>
                    </div>
                </div>
                <div className='row'>

                </div>
            </div>
        );
    }
}

export const ApplicationsPage = connect<ReduxStateProps, ReduxDispatchProps, ApplicationsPageProps>(
    (state: RootState, ownProps?: any) => ({}),
    (dispatch: Dispatch<RootState>, ownProps?: any) => bindActionCreators({}, dispatch)
)(UnconnectedApplicationsPage);