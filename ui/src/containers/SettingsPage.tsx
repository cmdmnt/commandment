import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {bindActionCreators} from 'redux';
import {IRootState} from "../reducers/index";
import { Container, Card, Icon } from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import {RouteComponentProps} from "react-router";

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
                    <Card as={Link} to='/settings/scep'>
                        <Card.Content>
                            <Card.Header>
                                <Icon name='protect' /> SCEP
                            </Card.Header>
                            <Card.Description>
                                Configure how communication is secured between your devices and this MDM
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
    (state: IRootState, ownProps?: any): ReduxStateProps => ({}),
    (dispatch: Dispatch<IRootState>): ReduxDispatchProps => bindActionCreators({}, dispatch)
)(UnconnectedSettingsPage);
