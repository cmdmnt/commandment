import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {RootState} from "../../reducers";

import Dropzone, {DropFilesEventHandler} from "react-dropzone";
import {Link} from "react-router-dom";

import {Component, SyntheticEvent} from "react";
import {RSAAApiErrorMessage} from "../../components/RSAAApiErrorMessage";
import {APNSState} from "../../store/configuration/apns_reducer";
import {
    csr,
    CsrActionRequest,
    uploadCrypted,
    UploadCryptedActionRequest,
} from "../../store/configuration/mdmcert_actions";

import {Breadcrumb, Button, Container, Divider, Header, Icon, Input, Message, Segment} from "semantic-ui-react";

interface IReduxStateProps {
    apns: APNSState;
}

interface IReduxDispatchProps {
    csr: CsrActionRequest;
    uploadCrypted: UploadCryptedActionRequest;
}

export type APNSPageProps = IReduxStateProps & IReduxDispatchProps & RouteComponentProps<any>;

interface IAPNSPageState {
    email: string;
}

export class UnconnectedAPNSPage extends Component<APNSPageProps, IAPNSPageState> {

    public state: IAPNSPageState = {email: ""};

    public render() {
        const {apns} = this.props;
        const mdmcertSuccess = apns && apns.csrResult && apns.csrResult.result === "success";

        return (
            <Container className="APNSPage">
                <Divider hidden/>
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider/>
                    <Breadcrumb.Section><Link to={`/settings`}>Settings</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider/>
                    <Breadcrumb.Section active>Push Certificate</Breadcrumb.Section>
                </Breadcrumb>

                <Header as="h1">Push Certificate</Header>
                <p>
                    A push certificate is required to tell devices to check in.
                    We use the site <strong>mdmcert.download</strong> to issue a Push Certificate.
                </p>
                <Segment vertical>
                    <Header>
                        <Icon name="signup" />
                        <Header.Content>
                            1. Register with mdmcert.download
                        </Header.Content>
                    </Header>

                    <a href="https://mdmcert.download/registration" target="_new">Register</a> a new e-mail address
                    with <strong>mdmcert.download</strong>. This e-mail will be used to send your signed certificate
                    request.
                </Segment>
                <Segment vertical>
                    <Header>
                        <Icon name="send" />
                        <Header.Content>
                            2. Get a certificate request signed and sent to this E-mail address
                        </Header.Content>
                    </Header>

                    <Input iconPosition="left" placeholder="Step 1 Registered E-mail" fluid value={this.state.email}
                           onChange={this.handleEmailChange} error={!this.state.email}
                           loading={apns && apns.csrLoading}>
                        <Icon name="mail"/>
                        <input/>
                    </Input>
                    <br/>
                    <Button primary onClick={this.handleSendMdmcertCsr}
                            disabled={apns && apns.csrLoading}>{mdmcertSuccess ? "Sent" : "Send"}</Button> a new encrypted certificate signing request
                    (.csr) to the e-mail
                    registered in step 1.

                    {apns && apns.csrResult && apns.csrResult.result === "failure" &&
                    <Message error>{apns.csrResult.reason}</Message>}
                    {apns && apns.csrResult && apns.csrResult.result === "success" &&
                    <Message success>OK, e-mail sent to the address above.</Message>}
                </Segment>
                <Segment vertical>
                    <Header>
                        <Icon name="upload" />
                        <Header.Content>
                            3. Save the attachment from the e-mail (.p7) and upload here
                        </Header.Content>
                    </Header>

                    <Dropzone onDrop={this.onDropEncryptedCSR}>
                        {({getRootProps, getInputProps, isDragActive}) => {
                            return (
                                <div
                                    {...getRootProps()}
                                    className={"dropzone"}
                                >
                                    <input {...getInputProps()} />
                                    {
                                        isDragActive ?
                                            <p>Drop files here...</p> :
                                            <p>Try dropping some files here, or click to select files to upload.<br />
                                                Expecting <strong>mdm_signed_request.(timestamp).plist.b64.p7</strong></p>
                                    }
                                </div>
                            )

                        }}
                    </Dropzone>
                    {apns && apns.decryptError && <RSAAApiErrorMessage error={apns.decryptError}/>}
                </Segment>
                <Segment vertical>
                    <Header>
                        <Icon name="download" />
                        <Header.Content>
                            4. Download
                        </Header.Content>
                    </Header>

                    <Button icon labelPosition="left">
                        <Icon name="download"/> Download
                    </Button> the decrypted Certificate Signing Request
                </Segment>
                <Segment vertical>
                    <Header>5. Upload to Push Portal</Header>

                    Upload the .csr to the <a href="https://identity.apple.com/pushcert/" target="_new">Apple Push
                    Portal</a>
                </Segment>
                <Segment vertical>
                    <Header>6. Download the push certificate from the Apple Push Portal</Header>
                </Segment>

            </Container>
        )
    }

    private handleSendMdmcertCsr = (e: any) => {
        if (this.state.email) {
            this.props.csr(this.state.email);
        }
    };

    private handleEmailChange = (e: SyntheticEvent<HTMLInputElement>) => {
        this.setState({email: e.currentTarget.value});
    };

    private onDropEncryptedCSR: DropFilesEventHandler = (accepted, rejected) => {
        console.dir(accepted);
        for (const file of accepted) {
            this.props.uploadCrypted(file);
        }
    };
}

export const APNSPage = connect<IReduxStateProps, IReduxDispatchProps, RouteComponentProps<any>>(
    (state: RootState): IReduxStateProps => ({
        apns: state.configuration.apns,
    }),
    (dispatch: Dispatch) => bindActionCreators({
        csr,
        uploadCrypted,
    }, dispatch),
)(UnconnectedAPNSPage);
