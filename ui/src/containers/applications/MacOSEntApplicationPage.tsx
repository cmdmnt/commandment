import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {
    post, PostActionRequest,
  //  read, ReadActionRequest
} from "../../store/applications/actions";
// import {ApplicationForm, IFormData, IFormData as ApplicationFormData} from "../../forms/ApplicationForm";
import {RootState} from "../../reducers";

interface IReduxStateProps {

}

interface IReduxDispatchProps {
    post: PostActionRequest;
}

interface IRouteParameters {
    platform: string;
    id?: string;
}

class UnconnectedApplicationPage extends React.Component<IReduxStateProps & IReduxDispatchProps & RouteComponentProps<IRouteParameters>, void> {

    public componentWillMount?() {
        if (this.props.match.params.id) {
            // this.props.read(this.props.match.params.id, ['applications']);
        }
    }

    // public handleSubmit = (values: IFormData) => {
    //     if (this.props.match.params.id) {
    //         // this.props.patch()
    //     } else {
    //         this.props.post(values);
    //     }
    // };

    public render() {
        const { } = this.props;

        return (
            <Container>
                <Header as="h1">Application</Header>
                {/*<ApplicationForm onSubmit={this.handleSubmit} onClickFetch={this.fetchManifestURL} />*/}
            </Container>
        );
    }

    public fetchManifestURL = (e: any) => {

    }
}

export const MacOSEntApplicationPage  = connect(
    (state: RootState, ownProps?: any) => ({}),
    (dispatch: Dispatch, ownProps?: any) => bindActionCreators({ post }, dispatch),
)(UnconnectedApplicationPage);
