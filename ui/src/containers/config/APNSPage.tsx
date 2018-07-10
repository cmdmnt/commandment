import * as React from 'react';
import {RouteComponentProps} from "react-router";
import Container from "semantic-ui-react/src/elements/Container/Container";
import Header from "semantic-ui-react/src/elements/Header/Header";
import {bindActionCreators} from "redux";
import {connect, Dispatch} from "react-redux";
import {RootState} from "../../reducers";

import Image from "semantic-ui-react/src/elements/Image/Image";
import Item from "semantic-ui-react/src/views/Item/Item";
import Icon from "semantic-ui-react/src/elements/Icon/Icon";
import Button from "semantic-ui-react/src/elements/Button/Button";


interface ReduxStateProps {

}

interface ReduxDispatchProps {

}

interface OwnProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<{}> {

}


export class UnconnectedAPNSPage extends React.Component {
    render() {
        return (
            <Container className="APNSPage">
                <Header as='h1'>Push Certificate</Header>
                <p>
                    A push certificate is required to tell devices to check in.
                </p>
                <Item.Group>
                    <Item>
                        <Item.Content>
                            <Item.Header>1. Register with mdmcert.download</Item.Header>
                            <Item.Description>
                                <a href="https://mdmcert.download/registration" target="_new">Register</a> a new e-mail address with mdmcert.download. This e-mail will be used to send
                                your signed certificate request.
                            </Item.Description>
                        </Item.Content>
                    </Item>

                    <Item>
                        <Item.Content>
                            <Item.Header>2. Send Request</Item.Header>
                            <Item.Description>
                                <Button primary>Request</Button> a new encrypted Certificate Signing Request. This will be delivered to your
                                e-mail.
                            </Item.Description>
                        </Item.Content>
                    </Item>

                    <Item>
                        <Item.Content>
                            <Item.Header>3. Decrypt</Item.Header>
                            <Item.Description>
                                <Button icon labelPosition="left">
                                    <Icon name='upload' /> Upload
                                </Button> the encrypted Signing Request
                            </Item.Description>
                        </Item.Content>
                    </Item>

                    <Item>
                        <Item.Content>
                            <Item.Header>4. Download</Item.Header>
                            <Item.Description>
                                <Button icon labelPosition="left">
                                    <Icon name='download' /> Download
                                </Button> the decrypted Certificate Signing Request
                            </Item.Description>
                        </Item.Content>
                    </Item>

                    <Item>
                        <Item.Content>
                            <Item.Header>5. Upload to Push Portal</Item.Header>
                            <Item.Description>
                                Upload the .csr to the <a href='https://identity.apple.com/pushcert/' target="_new">Apple Push Portal</a>
                            </Item.Description>
                        </Item.Content>
                    </Item>

                    <Item>
                        <Item.Content>
                            <Item.Header>6. Download from Push Portal</Item.Header>
                            <Item.Description>
                                <Button icon labelPosition="left">
                                    <Icon name='upload' /> Upload
                                </Button> the final certificate.
                            </Item.Description>
                        </Item.Content>
                    </Item>
                </Item.Group>
            </Container>
        )
    }
}


export const APNSPage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    (state: RootState): ReduxStateProps => ({

    }),
    (dispatch: Dispatch<any>) => bindActionCreators({

    }, dispatch)
)(UnconnectedAPNSPage);
