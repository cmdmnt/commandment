import * as React from 'react';
import {connect, Dispatch, MapStateToProps} from 'react-redux';
import {RouteComponentProps} from 'react-router';
import { SCEPConfigurationForm, FormData } from '../../../_deprecated/SCEPConfigurationForm';
import {SCEPPayloadForm} from '../../forms/payloads/SCEPPayloadForm';
import * as actions from '../../actions/configuration/scep';
import {RootState} from "../../reducers/index";
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
        this.props.post(values);
    };

    handleTest = () => {

    };

    render() {
        const {
            scep
        } = this.props;

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
    (state: RootState): ReduxStateProps => ({
        scep: state.configuration.scep
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        post: actions.post,
        read: actions.read
    }, dispatch)
)(UnconnectedSCEPPage);
