import * as React from "react";
import {connect, Dispatch, MapStateToProps} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import {DeviceAuthForm} from "../../forms/config/DeviceAuthForm";
import {FormData, SCEPPayloadForm} from "../../forms/payloads/SCEPPayloadForm";
import {RootState} from "../../reducers/index";
import * as actions from "../../store/configuration/scep_actions";
import {SCEPState} from "../../store/configuration/scep_reducer";

interface ReduxStateProps {
    scep: SCEPState;
}

interface ReduxDispatchProps {
    read: actions.ReadActionRequest;
    post: actions.PostActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<{}> {

}

export class UnconnectedDeviceAuthPage extends React.Component<OwnProps, undefined> {

    public componentWillMount?() {
        this.props.read();
    }

    private handleSubmit = (values: FormData): void => {
        this.props.post({
            ...values,
            key_usage: parseInt(values.key_usage, 0),
            key_size: parseInt(values.key_size, 0),
        });
    };

    private handleTest = () => {

    };

    public render() {
        const {
            scep,
        } = this.props;

        const stringifiedData = {
            ...scep.data,
            key_size: scep.data ? "" + scep.data.key_size : null,
            key_usage: scep.data ? "" + scep.data.key_usage : null,
        };

        return (
            <Container className="SCEPPage">
                <Header as="h1">Device Authentication</Header>
                <p>
                    Use this section to configure how your device will securely contact the MDM server.
                </p>
                <DeviceAuthForm />
            </Container>
        )
    }

}

export const DeviceAuthPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({
        scep: state.configuration.scep,
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        post: actions.post,
        read: actions.read,
    }, dispatch),
)(UnconnectedDeviceAuthPage);
