import * as React from 'react';
import {connect, Dispatch, MapStateToProps} from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {SCEPPayloadForm, FormData} from '../../forms/payloads/SCEPPayloadForm';
import * as actions from '../../actions/configuration/scep';
import {IRootState} from "../../reducers/index";
import {bindActionCreators} from "redux";
import {SCEPState} from "../../reducers/configuration/scep";
import {Container, Header} from 'semantic-ui-react';


interface ReduxStateProps {
    scep: SCEPState;
}

interface ReduxDispatchProps {
    read: actions.ReadActionRequest;
    post: actions.PostActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<{}> {

}

export class UnconnectedSCEPPage extends React.Component<OwnProps, undefined> {

    componentWillMount?() {
        this.props.read();
    }

    handleSubmit = (values: FormData): void => {
        this.props.post({
            ...values,
            key_usage: parseInt(values.key_usage, 0),
            key_size: parseInt(values.key_size, 0)
        });
    };

    handleTest = () => {

    };

    render() {
        const {
            scep
        } = this.props;

        const stringifiedData = {
            ...scep.data,
            key_size: scep.data ? ''+scep.data.key_size : null,
            key_usage: scep.data ? ''+scep.data.key_usage: null
        };

        return (
            <Container className='SCEPPage'>
                <Header as='h1'>SCEP Configuration</Header>
                        <p>
                            The SCEP Configuration controls the parameters of certificates issued to devices via your
                            SCEP service.
                        </p>
                        <SCEPPayloadForm
                            submitted={scep.submitted}
                            loading={scep.loading}
                            initialValues={scep.data}
                            onSubmit={this.handleSubmit}
                            onClickTest={this.handleTest}
                        />

            </Container>
        )
    }

}

export const SCEPPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: IRootState): ReduxStateProps => ({
        scep: state.configuration.scep
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        post: actions.post,
        read: actions.read
    }, dispatch)
)(UnconnectedSCEPPage);
