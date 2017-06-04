import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import * as actions from '../../actions/organization';
import {bindActionCreators} from "redux";
import {OrganizationState} from "../../reducers/organization";
import {OrganizationForm, FormData} from '../../forms/OrganizationForm';
import {RootState} from "../../reducers/index";
import {Segment, Header, Container} from 'semantic-ui-react';

interface OrganizationPageState {
    organization: OrganizationState;
}

function mapStateToProps(state: RootState, ownProps?: any): OrganizationPageState {
    return {
        organization: state.organization
    }
}

interface OrganizationPageDispatchProps {
    read: actions.ReadActionRequest;
    post: actions.PostActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>) {
    return bindActionCreators({
        post: actions.post,
        read: actions.read
    }, dispatch);
}

interface OrganizationPageProps extends OrganizationPageState, OrganizationPageDispatchProps, RouteComponentProps<any> {

}

@connect<OrganizationPageState, OrganizationPageDispatchProps, OrganizationPageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class OrganizationPage extends React.Component<OrganizationPageProps, undefined> {

    componentWillMount?() {
        this.props.read();
    }

    private handleSubmit: (values: FormData) => void = (values) => {
        this.props.post(values);
    };

    render(): JSX.Element {
        const {
            organization
        } = this.props;

        return (
            <Container className='OrganizationPage'>
                <Header as='h1'>Organization</Header>
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