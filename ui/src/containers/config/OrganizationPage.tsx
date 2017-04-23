import * as React from 'react';
import { connect, Dispatch } from 'react-redux';
import {RouteComponentProps} from 'react-router';
import * as actions from '../../actions/organization';
import {bindActionCreators} from "redux";
import {OrganizationState} from "../../reducers/organization";
import {OrganizationForm, FormData} from '../../forms/OrganizationForm';
import {RootState} from "../../reducers/index";

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

    componentWillMount() {
        this.props.read();
    }

    handleSubmit = (values: FormData): void => {
        this.props.post(values);
    };

    render(): JSX.Element {
        const {
            organization
        } = this.props;

        return (
            <div className='OrganizationPage container top-margin'>
                <div className='row'>
                    <div className='column'>
                        <h1>Organization</h1>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <OrganizationForm
                            initialValues={organization.organization}
                            onSubmit={this.handleSubmit}
                        />
                    </div>
                </div>
            </div>
        )
    }

}