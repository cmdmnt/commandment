import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {IRootState} from "../reducers/index";

interface ReduxStateProps {

}

interface ReduxDispatchProps {

}

interface ApplicationsPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {

}

interface ApplicationsPageState {
}

class UnconnectedApplicationsPage extends React.Component<ApplicationsPageProps, ApplicationsPageState> {
    public render() {
        return (
            <div className="ApplicationsPage top-margin container">
                <div className="row">
                    <div className="column">
                        <h1>Applications</h1>
                    </div>
                </div>
                <div className="row">

                </div>
            </div>
        );
    }
}

export const ApplicationsPage = connect<ReduxStateProps, ReduxDispatchProps, ApplicationsPageProps>(
    (state: IRootState, ownProps?: any) => ({}),
    (dispatch: Dispatch<IRootState>, ownProps?: any) => bindActionCreators({}, dispatch),
)(UnconnectedApplicationsPage);
