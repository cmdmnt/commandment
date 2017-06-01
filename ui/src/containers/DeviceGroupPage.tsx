import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RootState} from "../reducers/index";
import {bindActionCreators} from "redux";
import {Container, Segment, Header} from 'semantic-ui-react';
import {DeviceGroupForm} from "../forms/DeviceGroupForm";
import {post, PostActionRequest} from "../actions/device_groups";

interface ReduxStateProps {

}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {};
}

interface ReduxDispatchProps {
    post: PostActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>) {
    return bindActionCreators({
        post
    }, dispatch);
}

interface OwnProps {
}

@connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DeviceGroupPage extends React.Component<ReduxStateProps & ReduxDispatchProps & OwnProps, void> {

    handleSubmit = (values: FormData) => {
        console.log('adding group');
        this.props.post(values);
    };

    render() {
        const {

        } = this.props;

        return (
            <Container>
                <Header as='h1'>Device Group</Header>
                <DeviceGroupForm onSubmit={this.handleSubmit} />
            </Container>
        )
    }
}