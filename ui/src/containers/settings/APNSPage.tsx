import * as React from 'react';
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {connect, Dispatch} from "react-redux";
import {RootState} from "../../reducers";

import Dropzone, {DropFilesEventHandler} from "react-dropzone";
import Container from "semantic-ui-react/src/elements/Container/Container";
import Header from "semantic-ui-react/src/elements/Header/Header";
import Segment from "semantic-ui-react/src/elements/Segment/Segment";
import Icon from "semantic-ui-react/src/elements/Icon/Icon";
import Button from "semantic-ui-react/src/elements/Button/Button";
import Input from "semantic-ui-react/src/elements/Input/Input";

import {csr, CsrActionRequest, uploadCrypted, UploadCryptedActionRequest} from "../../actions/settings/mdmcert";
import {SyntheticEvent} from "react";
import {RSAAApiErrorMessage} from "../../components/RSAAApiErrorMessage";
import {APNSState} from "../../reducers/settings/apns";


interface ReduxStateProps {
    apns: APNSState;
}

interface ReduxDispatchProps {
    csr: CsrActionRequest;
    uploadCrypted: UploadCryptedActionRequest;
}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<{}> {

}

interface APNSPageState {
    email: string;
}


export class UnconnectedAPNSPage extends React.Component<OwnProps> {

    public state: APNSPageState = { email: "" };

    handleSendMdmcertCsr = (e: any) => {
        if (this.state.email) {
            this.props.csr(this.state.email);
        }
    };

    handleEmailChange = (e: SyntheticEvent<HTMLInputElement>) => {
        this.setState({ email: e.currentTarget.value });
    };

    onDropEncryptedCSR: DropFilesEventHandler = (accepted, rejected) => {
        console.dir(accepted);
        for (let file of accepted) {
            this.props.uploadCrypted(file);
        }
    };

    render() {
        return (
            <Container className="APNSPage">
                <Header as='h1'>Push Certificate</Header>
                <p>
                    A push certificate is required to tell devices to check in.
                </p>
                <Segment vertical>
                    <Header>1. Register with mdmcert.download</Header>

                    <a href="https://mdmcert.download/registration" target="_new">Register</a> a new e-mail address
                    with <strong>mdmcert.download</strong>. This e-mail will be used to send your signed certificate
                    request.
                </Segment>
                <Segment vertical>
                    <Header>2. Send Request</Header>

                    <Input iconPosition='left' placeholder='Step 1 Registered E-mail' fluid value={this.state.email}
                           onChange={this.handleEmailChange} error={!this.state.email} loading={this.props.apns.csrLoading}>
                        <Icon name='mail' />
                        <input />
                    </Input>
                    <br />
                    <Button primary onClick={this.handleSendMdmcertCsr} disabled={this.props.apns.csrLoading}>Send</Button> a new encrypted certificate signing request (.csr) to the e-mail
                    registered in step 1.
                    {this.props.apns.error && <RSAAApiErrorMessage error={this.props.apns.error} />}
                </Segment>
                <Segment vertical>
                    <Header>3. Save the attachment (.p7) and upload here</Header>

                    <Dropzone onDrop={this.onDropEncryptedCSR} />
                    {/*<input type="file" name="file" />*/}
                    {/*<Button icon labelPosition="left">*/}
                        {/*<Icon name='upload' /> Upload*/}
                    {/*</Button> the encrypted Signing Request*/}
                </Segment>
                <Segment vertical>
                    <Header>4. Download</Header>

                    <Button icon labelPosition="left">
                        <Icon name='download' /> Download
                    </Button> the decrypted Certificate Signing Request
                </Segment>
                <Segment vertical>
                    <Header>5. Upload to Push Portal</Header>

                    Upload the .csr to the <a href='https://identity.apple.com/pushcert/' target="_new">Apple Push Portal</a>
                </Segment>
                <Segment vertical>
                    <Header>6. Download from Push Portal</Header>

                    {/*<Button icon labelPosition="left" as="input" htmlType="upload">*/}
                        {/*<Icon name='upload' /> Upload*/}
                    {/*</Button> the final certificate.*/}
                </Segment>

            </Container>
        )
    }
}


export const APNSPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({
        apns: state.configuration.apns
    }),
    (dispatch: Dispatch<any>) => bindActionCreators({
        csr,
        uploadCrypted,
    }, dispatch)
)(UnconnectedAPNSPage);
