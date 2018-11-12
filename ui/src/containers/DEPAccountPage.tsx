import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {Link} from "react-router-dom";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import List from "semantic-ui-react/dist/commonjs/elements/List/List";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import {RootState} from "../reducers";
import {DEPAccountState} from "../store/dep/account_reducer";
import {account, AccountReadActionRequest} from "../store/dep/actions";
import {DEPProfilesTable} from "../components/griddle-tables/DEPProfilesTable";

interface IOwnProps {

}

interface IReduxStateProps {
    dep_account?: DEPAccountState;
}

interface IReduxDispatchProps {
    getAccount: AccountReadActionRequest;
}

interface IRouteParameters {
    id?: string;
}

interface IDEPAccountPageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<IRouteParameters> {

}

interface IDEPAccountPageState {

}

class UnconnectedDEPAccountPage extends React.Component<IDEPAccountPageProps, IDEPAccountPageState> {

    componentWillMount() {
        this.props.getAccount(this.props.match.params.id, ["dep_profiles"]);
    }

    render() {

        const {
            dep_account: {
                loading,
                error,
                dep_account,
                dep_profiles,
            },
        } = this.props;

        const title = (dep_account && !loading) ? dep_account.attributes.server_name : "DEP Account (loading)";

        return (
            <Container className="DEPAccountPage">

                <Header as="h1">{title}</Header>

                {dep_account && !loading &&
                <div>
                  <List divided>
                    <List.Item>
                      <List.Content>
                        <List.Header>Server Name (As shown in Apple School Manager or Apple Business
                          Manager)</List.Header>
                        <List.Description>{dep_account.attributes.server_name}</List.Description>
                      </List.Content>
                    </List.Item>
                    <List.Item>
                      <List.Content>
                        <List.Header>Administrator Apple ID</List.Header>
                        <List.Description>{dep_account.attributes.admin_id}</List.Description>
                      </List.Content>
                    </List.Item>
                  </List>
                  <Segment>
                    <Header as="h3">Organization</Header>
                    <List>
                      <List.Item icon="building" description={dep_account.attributes.org_name}/>
                      <List.Item icon="compass" description={dep_account.attributes.org_address}/>
                      <List.Item icon="mail" description={dep_account.attributes.org_email}/>
                      <List.Item icon="mobile" description={dep_account.attributes.org_phone}/>
                    </List>
                  </Segment>

                  <Link to={`/dep/accounts/${dep_account.id}/add/profile`}>New DEP Profile</Link>
                    
                  <DEPProfilesTable depAccountId={dep_account.id} data={dep_profiles} />
                </div>
                }
            </Container>
        );
    }
}

export const DEPAccountPage = connect<IReduxStateProps, IReduxDispatchProps, IOwnProps>(
    (state: RootState, ownProps: IOwnProps): IReduxStateProps => {
        return {dep_account: state.dep.account};
    },
    (dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        getAccount: account,
    }, dispatch),
)(UnconnectedDEPAccountPage);
