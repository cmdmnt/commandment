import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RootState} from "../reducers";
import {bindActionCreators} from "redux";
import {RouteComponentProps} from "react-router";
import * as apiActions from "../actions/certificates";
import Container from "semantic-ui-react/src/elements/Container/Container";

interface OwnProps {

}

interface ReduxStateProps {

}

function mapStateToProps(state: RootState, ownProps: OwnProps): ReduxStateProps {
    return { };
}

interface ReduxDispatchProps {

}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps: OwnProps): ReduxDispatchProps {
    return bindActionCreators({

    }, dispatch);
}

interface DashboardPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {

}

interface DashboardPageState {

}

class BaseDashboardPage extends React.Component<DashboardPageProps, DashboardPageState> {
    render() {
        return (
            <Container className="DashboardPage">
                <ul>
                    <li> <a href="/enroll/profile">Enroll (Direct)</a></li>
                    <li> <a href="/enroll/ota">Enroll (OTA)</a></li>
                    <li> <a href="/enroll/trust.mobileconfig">Download Trust Profile</a></li>
                </ul>
            </Container>
        )
    }

}

export const DashboardPage = connect<ReduxStateProps, ReduxDispatchProps, DashboardPageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(BaseDashboardPage);
