import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {Link} from "react-router-dom";
import {bindActionCreators, Dispatch} from "redux";
import {DEPProfilesTable} from "../components/react-tables/DEPProfilesTable";
import {ButtonLink} from "../components/semantic-ui/ButtonLink";
import {RootState} from "../reducers";
import {IDEPAccountState} from "../store/dep/account_reducer";
import {account, AccountReadActionCreator} from "../store/dep/actions";

import {
    Breadcrumb,
    Container,
    Divider,
    Header,
    List,
    Segment,
} from "semantic-ui-react";

import {IReactTableState} from "../store/table/types";
import {FlaskFilterOperation} from "../flask-rest-jsonapi";
import {FlaskFilter} from "../flask-rest-jsonapi";

interface IReduxStateProps {
    dep_account?: IDEPAccountState;
}

interface IReduxDispatchProps {
    getAccount: AccountReadActionCreator;
}

interface IRouteParameters {
    id?: string;
}

interface IDEPAccountPageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<IRouteParameters> {

}

class UnconnectedDEPAccountPage extends React.Component<IDEPAccountPageProps, any> {

    public componentWillMount() {
        this.props.getAccount(this.props.match.params.id, ["dep_profiles"]);
    }

    public render() {

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
                <Divider hidden />
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section><Link to={`/settings`}>Settings</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section><Link to={`/settings/dep/accounts`}>DEP Accounts</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section active>{loading ? "DEP Account" : title}</Breadcrumb.Section>
                </Breadcrumb>

                <Header as="h1">{title}</Header>

                {dep_account && !loading &&
                <div>
                    <Segment.Group>
                        <Segment attached>
                          <Header as="h3">Overview</Header>
                          <List>
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
                        </Segment>
                        <Segment attached>
                            <Header as="h3">Organization</Header>
                            <List>
                              <List.Item icon="building" description={dep_account.attributes.org_name}/>
                              <List.Item icon="compass" description={dep_account.attributes.org_address}/>
                              <List.Item icon="mail" description={dep_account.attributes.org_email}/>
                              <List.Item icon="mobile" description={dep_account.attributes.org_phone}/>
                            </List>
                        </Segment>
                    </Segment.Group>

                  <Header as="h3">Profiles</Header>
                  <ButtonLink to={`/dep/accounts/${dep_account.id}/add/profile`}>New DEP Profile</ButtonLink>

                  <DEPProfilesTable
                    data={dep_profiles}
                  />
                </div>
                }
            </Container>
        );
    }
}

export const DEPAccountPage = connect<IReduxStateProps, IReduxDispatchProps, any>(
    (state: RootState, ownProps: any): IReduxStateProps => {
        return {dep_account: state.dep.account};
    },
    (dispatch: Dispatch, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        getAccount: account,
    }, dispatch),
)(UnconnectedDEPAccountPage);
