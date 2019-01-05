import * as React from "react";
import {Link, Route} from "react-router-dom";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import {RootState} from "../reducers";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {ButtonLink} from "../components/semantic-ui/ButtonLink";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

class UnconnectedApplicationsPage extends React.Component<RouteComponentProps<any>, any> {
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

export const ApplicationsPage = connect(
    (state: RootState, ownProps?: any) => ({}),
    (dispatch: Dispatch, ownProps?: any) => bindActionCreators({}, dispatch),
)(UnconnectedApplicationsPage);
