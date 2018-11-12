import * as React from "react";

import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {FormProps} from "semantic-ui-react";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {DEPProfileForm, IDEPProfileFormValues} from "../components/forms/DEPProfileForm";
import {RootState} from "../reducers";
import {postProfile, profile, ProfilePostActionRequest, ProfileReadActionRequest} from "../store/dep/actions";
import {IDEPProfileState} from "../store/dep/profile_reducer";
import {DEPProfile, SkipSetupSteps} from "../store/dep/types";
import Message from "semantic-ui-react/dist/commonjs/collections/Message/Message";
import {RSAAApiErrorMessage} from "../components/RSAAApiErrorMessage";

interface IReduxStateProps {
    dep_profile?: IDEPProfileState;
}

interface IReduxDispatchProps {
    getDEPProfile: ProfileReadActionRequest;
    postDEPProfile: ProfilePostActionRequest;
}

interface IRouteParameters {
    account_id: string;
    id?: string;
}

interface IDEPProfilePageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<IRouteParameters> {

}

class UnconnectedDEPProfilePage extends React.Component<IDEPProfilePageProps, void> {

    public componentWillMount() {
        const {
            match: {
                params: {
                    id,
                },
            },
        } = this.props;

        if (id && id !== "add") {
            this.props.getDEPProfile(this.props.match.params.id);
        }
    }

    public render() {
        const {
            dep_profile,
            match: {
                params: {
                    id,
                },
            },
        } = this.props;

        let title = "loading";
        if (id && id !== "add") {
            title = `Edit ${this.props.dep_profile.dep_profile ?
                this.props.dep_profile.dep_profile.attributes.profile_name : "Loading..."}`;
        } else {
            title = "Create a new DEP Profile";
        }

        return (
            <Container className="DEPProfilePage">
                <Header as="h1">{title}</Header>
                {dep_profile.error && <RSAAApiErrorMessage error={dep_profile.errorDetail} />}
                <DEPProfileForm onSubmit={this.handleSubmit}
                                loading={dep_profile.loading}
                                data={dep_profile.dep_profile && dep_profile.dep_profile.attributes} />
            </Container>
        );
    }

    private handleSubmit = (values: IDEPProfileFormValues) => {
        const { show, ...profile } = values;
        profile.skip_setup_items = [];

        if (show) {
            for (const kskip in SkipSetupSteps) {
                if (!show[kskip]) {
                    profile.skip_setup_items.unshift(kskip as SkipSetupSteps);
                }
            }
        }

        profile.url = "http://test.something/dep/enroll"; // TODO: THIS IS A PLACEHOLDER

        this.props.postDEPProfile(profile, {
            dep_account: { type: "dep_accounts", id: this.props.match.params.account_id } });
    };
}

export const DEPProfilePage = connect(
    (state: RootState, ownProps: any): IReduxStateProps => {
        return {dep_profile: state.dep.profile};
    },
    (dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        getDEPProfile: profile,
        postDEPProfile: postProfile,
    }, dispatch),
)(UnconnectedDEPProfilePage);
