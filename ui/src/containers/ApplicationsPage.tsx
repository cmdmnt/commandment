import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import {RootState} from "../reducers";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {ButtonLink} from "../components/semantic-ui/ButtonLink";

interface IReduxStateProps {

}

interface IReduxDispatchProps {

}

interface IApplicationsPageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<any> {

}

interface IApplicationsPageState {
}

class UnconnectedApplicationsPage extends React.Component<IApplicationsPageProps, IApplicationsPageState> {
    render() {
        return (
            <Container className="ApplicationsPage">
                <Grid>
                    <Grid.Column>
                      <Header as="h1">Applications</Header>
                        <ButtonLink to="/applications/add/macos">Add new Application</ButtonLink>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}

export const ApplicationsPage = connect<IReduxStateProps, IReduxDispatchProps, IApplicationsPageProps>(
    (state: RootState, ownProps?: any) => ({}),
    (dispatch: Dispatch<RootState>, ownProps?: any) => bindActionCreators({}, dispatch),
)(UnconnectedApplicationsPage);
