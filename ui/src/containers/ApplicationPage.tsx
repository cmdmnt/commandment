import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {
    post, PostActionRequest,
  //  read, ReadActionRequest
} from "../store/applications/actions";
import {ApplicationForm, IFormData, IFormData as ApplicationFormData} from "../forms/ApplicationForm";
import {RootState} from "../reducers";

interface IReduxStateProps {

}

interface IReduxDispatchProps {
    post: PostActionRequest;
}

interface IRouteParameters {
    platform: string;
}

interface IOwnProps extends RouteComponentProps<IRouteParameters> {

}

class UnconnectedApplicationPage extends React.Component<IReduxStateProps & IReduxDispatchProps & IOwnProps, void> {

    public componentWillMount?() {
        if (this.props.match.params.id) {
            // this.props.read(this.props.match.params.id, ['applications']);
        }
    }

    public handleSubmit = (values: IFormData) => {
        if (this.props.match.params.id) {
            // this.props.patch()
        } else {
            this.props.post(values);
        }
    }

    public render() {
        const { } = this.props;

        return (
            <Container>
                <Header as="h1">Application</Header>
                <ApplicationForm onSubmit={this.handleSubmit} onClickFetch={this.fetchManifestURL} />
            </Container>
        );
    }

    public fetchManifestURL = (e: any) => {

    }
}

export const ApplicationPage  = connect(
    (state: RootState, ownProps?: IOwnProps) => ({}),
    (dispatch: Dispatch<RootState>, ownProps?: IOwnProps) => bindActionCreators({ post }, dispatch),
)(UnconnectedApplicationPage);
