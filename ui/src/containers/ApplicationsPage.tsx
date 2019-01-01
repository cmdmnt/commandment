import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {Link, Route} from "react-router-dom";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import {RootState} from "../reducers";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {ButtonLink} from "../components/semantic-ui/ButtonLink";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

interface IReduxStateProps {

}

interface IReduxDispatchProps {

}

interface IApplicationsPageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<any> {

}

interface IApplicationsPageState {
}

class UnconnectedApplicationsPage extends React.Component<IApplicationsPageProps, IApplicationsPageState> {
    public render() {
        return (
            <Container className="ApplicationsPage">
                <Divider hidden />

                <Header as="h1">Applications</Header>
                <Dropdown text="Add" icon="plus" labeled button className="icon">
                    <Dropdown.Menu>
                        <Dropdown.Item as={Link} to="/applications/add/macos">macOS Enterprise Package
                            (.pkg)</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications/add/mas" disabled>macOS App Store
                            Application</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications/add/ias" disabled>iOS App Store
                            Application</Dropdown.Item>
                        <Dropdown.Item as={Link} to="/applications/add/ios" disabled>iOS Enterprise Application
                            (.ipa)</Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>

            </Container>
        );
    }
}

export const ApplicationsPage = connect<IReduxStateProps, IReduxDispatchProps, IApplicationsPageProps>(
    (state: RootState, ownProps?: any) => ({}),
    (dispatch: Dispatch<RootState>, ownProps?: any) => bindActionCreators({}, dispatch),
)(UnconnectedApplicationsPage);
