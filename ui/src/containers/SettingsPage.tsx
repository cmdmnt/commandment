import * as React from "react";
import {Link, RouteComponentProps} from "react-router-dom";

import {
    Divider,
    Container,
    Header,
    Icon,
    Card,
} from "semantic-ui-react";

export const SettingsPage: React.FunctionComponent<any> = () => (
    <Container>
        <Divider hidden/>
        <Header>General</Header>
        <Card.Group>
            <Card as={Link} to="/settings/organization">
                <Card.Content>
                    <Card.Header>
                        <Icon name="building" /> Organization
                    </Card.Header>
                    <Card.Description>
                        Configure your organization
                    </Card.Description>
                </Card.Content>
            </Card>
            <Card as={Link} to="/settings/deviceauth">
                <Card.Content>
                    <Card.Header>
                        <Icon name="protect" /> Device Authentication
                    </Card.Header>
                    <Card.Description>
                        Configure how communication is secured between your devices and this MDM
                    </Card.Description>
                </Card.Content>
            </Card>
            <Card as={Link} to="/settings/apns">
                <Card.Content>
                    <Card.Header>
                        <Icon name="cloud upload" /> Push Certificate
                    </Card.Header>
                    <Card.Description>
                        Configure a Push Certificate
                    </Card.Description>
                </Card.Content>
            </Card>
            <Card as={Link} to="/settings/authentication">
                <Card.Content>
                    <Card.Header>
                        <Icon name="users" /> Authentication
                    </Card.Header>
                    <Card.Description>
                        Configure authentication sources
                    </Card.Description>
                </Card.Content>
            </Card>

        </Card.Group>
        <Header>Enrollment</Header>
        <Card.Group>
            <Card as={Link} to="/settings/vpp">
                <Card.Content>
                    <Card.Header>
                        <Icon name="credit card alternative" /> VPP Accounts
                    </Card.Header>
                    <Card.Description>
                        Configure access to the Volume Purchasing Programme
                    </Card.Description>
                </Card.Content>
            </Card>
            <Card as={Link} to="/settings/dep/accounts">
                <Card.Content>
                    <Card.Header>
                        <Icon name="tablet" /> DEP Accounts
                    </Card.Header>
                    <Card.Description>
                        Configure the Device Enrollment Programme
                    </Card.Description>
                </Card.Content>
            </Card>
        </Card.Group>
    </Container>
);
