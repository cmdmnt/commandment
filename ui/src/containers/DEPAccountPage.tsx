import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {DEPAccount} from "../models";
import {RouteComponentProps} from "react-router";
import {read, ReadActionRequest} from "../actions/settings/dep";
import {RootState} from "../reducers";
import * as actions from "../actions/profiles";
import {bindActionCreators} from "redux";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import List from "semantic-ui-react/dist/commonjs/elements/List/List";
import {DEPAccountState} from "../reducers/dep/account";

interface IOwnProps {

}

interface IReduxStateProps {
    dep_account?: DEPAccountState;
}

interface IReduxDispatchProps {
    read: ReadActionRequest;
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
        this.props.read(this.props.match.params.id);
    }

    render() {

        const {
            dep_account: {
                loading,
                error,
                dep_account
            }
        } = this.props;

        const title = (dep_account && !loading) ? dep_account.attributes.server_name : 'DEP Account (loading)';

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
                </div>
                }
            </Container>
        )
    }
}

export const DEPAccountPage = connect<IReduxStateProps, IReduxDispatchProps, IOwnProps>(
    (state: RootState, ownProps: IOwnProps): IReduxStateProps => {
        return {dep_account: state.dep_account};
    },
    (dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        read
    }, dispatch),
)(UnconnectedDEPAccountPage);


