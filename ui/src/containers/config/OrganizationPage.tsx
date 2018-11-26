import * as React from "react";
import { connect, Dispatch } from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {FormData, OrganizationForm} from "../../forms/config/OrganizationForm";
import {RootState} from "../../reducers/index";
import * as actions from "../../store/organization/actions";
import {OrganizationState} from "../../store/organization/reducer";

interface OrganizationPageState {
    organization: OrganizationState;
}

function mapStateToProps(state: RootState, ownProps?: any): OrganizationPageState {
    return {
        organization: state.organization,
    }
}

interface OrganizationPageDispatchProps {
    read: actions.ReadActionRequest;
    post: actions.PostActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>) {
    return bindActionCreators({
        post: actions.post,
        read: actions.read,
    }, dispatch);
}

interface OrganizationPageProps extends OrganizationPageState, OrganizationPageDispatchProps, RouteComponentProps<any> {

}

export class UnconnectedOrganizationPage extends React.Component<OrganizationPageProps, undefined> {

    componentWillMount?() {
        this.props.read();
    }

    private handleSubmit: (values: FormData) => void = (values) => {
        this.props.post(values);
    };

    render(): JSX.Element {
        const {
            organization,
        } = this.props;

        return (
            <Container className="OrganizationPage">
                <Header as="h1">Organization</Header>
                <p>Many parts of the system rely on showing your organization name in certain user facing scenarios.
                    Configure these details here</p>
                <OrganizationForm
                    loading={organization.loading}
                    submitted={organization.submitted}
                    initialValues={organization.organization}
                    onSubmit={this.handleSubmit}
                />

            </Container>
        )
    }

}

export const OrganizationPage = connect<OrganizationPageState, OrganizationPageDispatchProps, OrganizationPageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedOrganizationPage);
