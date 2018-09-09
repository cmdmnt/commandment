import * as React from "react";
import {connect, Dispatch, MapStateToProps} from "react-redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {DEPState} from "../../reducers/configuration/dep";
import {RootState} from "../../reducers/index";
import {DEPAccountsTable} from "../../components/griddle-tables/DEPAccountsTable";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import {Link} from "react-router-dom";
import Grid from "semantic-ui-react/dist/commonjs/collections/Grid/Grid";
import {
    IndexActionRequest, index
} from "../../actions/settings/dep";

interface RouteProps {

}

interface ReduxStateProps {
    dep: DEPState;
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteProps> {

}

export class UnconnectedDEPAccountsPage extends React.Component<OwnProps, void> {

    componentWillMount?() {
        this.props.index();
    }


    render() {
        const {
            dep: {data, loading},
        } = this.props;

        return (
            <Container className="DEPAccountsPage">
                <Header as="h1">DEP Accounts</Header>
                <Grid>
                    <Grid.Column>
                        <Dropdown text="Add" icon="plus" labeled button className="icon">
                            <Dropdown.Menu>
                                <Dropdown.Item as={Link} to="/settings/dep/accounts/add">New DEP Account</Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    </Grid.Column>
                </Grid>
                <DEPAccountsTable data={[]} />
            </Container>
        );
    }
}

export const DEPAccountsPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({
        dep: state.configuration.dep,
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        index
    }, dispatch),
)(UnconnectedDEPAccountsPage);