import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {bindActionCreators} from 'redux';
import {RootState} from "../reducers/index";
import Container from "semantic-ui-react/src/elements/Container";
import Card from "semantic-ui-react/src/views/Card";
import Icon from "semantic-ui-react/src/elements/Icon";

import {Link} from 'react-router-dom';
import {RouteComponentProps} from "react-router";
import Header from "semantic-ui-react/src/elements/Header/Header";

interface RouteProps {

}

interface ReduxStateProps {

}

interface ReduxDispatchProps {

}

interface SettingsPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteProps> {

}

export class UnconnectedSettingsPage extends React.Component<SettingsPageProps, void | Readonly<{}>> {

    render() {
        const {

        } = this.props;

        return (
            <Container>
                <Header>General</Header>
                <Card.Group>
                    <Card as={Link} to='/settings/organization'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='building' /> Organization
                            </Card.Header>
                            <Card.Description>
                                Configure your organization
                            </Card.Description>
                        </Card.Content>
                    </Card>
                    <Card as={Link} to='/settings/deviceauth'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='protect' /> Device Authentication
                            </Card.Header>
                            <Card.Description>
                                Configure how communication is secured between your devices and this MDM
                            </Card.Description>
                        </Card.Content>
                    </Card>
                    <Card as={Link} to='/settings/apns'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='cloud upload' /> Push Certificate
                            </Card.Header>
                            <Card.Description>
                                Configure a Push Certificate
                            </Card.Description>
                        </Card.Content>
                    </Card>
                    <Card as={Link} to='/settings/authentication'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='users' /> Authentication
                            </Card.Header>
                            <Card.Description>
                                Configure authentication sources
                            </Card.Description>
                        </Card.Content>
                    </Card>

                </Card.Group>
                <Header>Enrollment</Header>
                <Card.Group>
                    <Card as={Link} to='/settings/vpp'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='credit card alternative' /> VPP
                            </Card.Header>
                            <Card.Description>
                                Configure access to the Volume Purchasing Programme
                            </Card.Description>
                        </Card.Content>
                    </Card>
                    <Card as={Link} to='/settings/dep'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='tablet' /> DEP
                            </Card.Header>
                            <Card.Description>
                                Configure the Device Enrollment Programme
                            </Card.Description>
                        </Card.Content>
                    </Card>
                </Card.Group>
            </Container>
        );
    }
}

export const SettingsPage = connect<ReduxStateProps, ReduxDispatchProps, SettingsPageProps>(
    (state: RootState, ownProps?: any): ReduxStateProps => ({}),
    (dispatch: Dispatch<RootState>): ReduxDispatchProps => bindActionCreators({}, dispatch)
)(UnconnectedSettingsPage);
