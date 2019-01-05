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
import {csr, CsrActionRequest, uploadCrypted, UploadCryptedActionRequest} from "../../store/configuration/mdmcert_actions";

import Breadcrumb from "semantic-ui-react/dist/commonjs/collections/Breadcrumb/Breadcrumb";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import Button from "semantic-ui-react/src/elements/Button/Button";
import Container from "semantic-ui-react/src/elements/Container/Container";
import Header from "semantic-ui-react/src/elements/Header/Header";
import Icon from "semantic-ui-react/src/elements/Icon/Icon";
import Input from "semantic-ui-react/src/elements/Input/Input";
import Segment from "semantic-ui-react/src/elements/Segment/Segment";

interface IReduxStateProps {
    apns: APNSState;
}

interface IReduxDispatchProps {
    csr: CsrActionRequest;
    uploadCrypted: UploadCryptedActionRequest;
}

interface OwnProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<any> {

}

interface APNSPageState {
    email: string;
}

export class UnconnectedAPNSPage extends Component<OwnProps> {

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
        for (const file of accepted) {
            this.props.uploadCrypted(file);
        }
    };

    render() {
        return (
            <Container className="APNSPage">
                <Divider hidden />
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section><Link to={`/settings`}>Settings</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section active>Push Certificate</Breadcrumb.Section>
                </Breadcrumb>

                <Header as="h1">Push Certificate</Header>
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

                    <Input iconPosition="left" placeholder="Step 1 Registered E-mail" fluid value={this.state.email}
                           onChange={this.handleEmailChange} error={!this.state.email} loading={this.props.apns.csrLoading}>
                        <Icon name="mail" />
                        <input />
                    </Input>
                    <br />
                    <Button primary onClick={this.handleSendMdmcertCsr} disabled={this.props.apns.csrLoading}>Send</Button> a new encrypted certificate signing request (.csr) to the e-mail
                    registered in step 1.
                    {this.props.apns.error && <RSAAApiErrorMessage error={this.props.apns.error} />}
                </Segment>
                <Segment vertical>
                    <Header>3. Save the attachment (.p7) and upload here</Header>

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
                                            <p>Try dropping some files here, or click to select files to upload.</p>
                                    }
                                </div>
                            )

                        }}
                    </Dropzone>
                </Segment>
                <Segment vertical>
                    <Header>4. Download</Header>

                    <Button icon labelPosition="left">
                        <Icon name="download" /> Download
                    </Button> the decrypted Certificate Signing Request
                </Segment>
                <Segment vertical>
                    <Header>5. Upload to Push Portal</Header>

                    Upload the .csr to the <a href="https://identity.apple.com/pushcert/" target="_new">Apple Push Portal</a>
                </Segment>
                <Segment vertical>
                    <Header>6. Download the push certificate from the Apple Push Portal</Header>
                </Segment>

            </Container>
        )
    }
}

export const APNSPage = connect<IReduxStateProps, IReduxDispatchProps, OwnProps>(
    (state: RootState): IReduxStateProps => ({
        apns: state.configuration.apns,
    }),
    (dispatch: Dispatch) => bindActionCreators({
        csr,
        uploadCrypted,
    }, dispatch),
)(UnconnectedAPNSPage);
