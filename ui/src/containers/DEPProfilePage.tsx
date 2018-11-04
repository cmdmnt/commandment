import * as React from "react";

import {profile, ProfileReadActionRequest} from "../store/dep/actions";
import {RouteComponentProps} from "react-router";
import {connect, Dispatch} from "react-redux";
import {IDEPProfileState} from "../store/dep/profile_reducer";
import {RootState} from "../reducers";
import {bindActionCreators} from "redux";
import {DEPProfileForm} from "../components/forms/DEPProfileForm";
import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import {FormProps} from "semantic-ui-react";
import {DEPProfile} from "../store/dep/types";


interface IReduxStateProps {
    dep_profile?: IDEPProfileState;
}

interface IReduxDispatchProps {
    getDEPProfile: ProfileReadActionRequest;
}

interface IRouteParameters {
    account_id: string;
    id?: string;
}

interface IDEPProfilePageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<IRouteParameters> {

}

class UnconnectedDEPProfilePage extends React.Component<IDEPProfilePageProps, void> {

    handleSubmit = (data: DEPProfile) => {
        console.dir(data);
    };

    render() {
        const {
            dep_profile
        } = this.props;

        let title = "loading";
        if (this.props.match.params.id) {

        } else {
            title = "Create a new DEP Profile"
        }

        return (
            <Container className="DEPProfilePage">
                <Header as="h1">{title}</Header>
                <DEPProfileForm onSubmit={this.handleSubmit} />
            </Container>
        )
    }
}

export const DEPProfilePage = connect(
    (state: RootState, ownProps: any): IReduxStateProps => {
        return {dep_profile: state.dep.profile};
    },
    (dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        getDEPProfile: profile
    }, dispatch),
)(UnconnectedDEPProfilePage);
