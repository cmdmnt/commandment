import * as React from 'react';
import {RouteComponentProps} from "react-router";
import {connect, Dispatch} from "react-redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {ApplicationForm, FormData as ApplicationFormData} from "../forms/ApplicationForm";
import {
    post, PostActionRequest,
  //  read, ReadActionRequest
} from "../actions/applications";
import {RootState} from "../reducers/index";
import {bindActionCreators} from "redux";

interface ReduxStateProps {

}

interface ReduxDispatchProps {
    post: PostActionRequest;
}

interface RouteParameters {
    id?: string;
}

interface OwnProps extends RouteComponentProps<RouteParameters> {
    
}

class UnconnectedApplicationPage extends React.Component<ReduxStateProps & ReduxDispatchProps & OwnProps, void> {

    componentWillMount?() {
        if (this.props.match.params.id) {
            // this.props.read(this.props.match.params.id, ['applications']);
        }
    }

    handleSubmit = (values: ApplicationFormData) => {
        if (this.props.match.params.id) {
            // this.props.patch()
        } else {
            this.props.post(values);
        }
    };

    render() {
        const { } = this.props;

        return (
            <Container>
                <Header as='h1'>Application</Header>
                <ApplicationForm onSubmit={this.handleSubmit} />
            </Container>
        )
    }
}

export const ApplicationPage  = connect(
    (state: RootState, ownProps?: OwnProps) => ({}),
    (dispatch: Dispatch<RootState>, ownProps?: OwnProps) => bindActionCreators({ post }, dispatch),
)(UnconnectedApplicationPage);