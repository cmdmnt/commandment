import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {bindActionCreators} from 'redux';
import {RootState} from "../reducers/index";
import { Container, Card, Icon } from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import {RouteComponentProps} from "react-router";

interface RouteProps {

}

interface ReduxStateProps {

}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {};
}

interface ReduxDispatchProps {

}

function mapDispatchToProps(dispatch: Dispatch<RootState>): ReduxDispatchProps {
    return bindActionCreators({}, dispatch);
}

interface SettingsPageProps extends RouteComponentProps<RouteProps> {

}

@connect<ReduxStateProps, ReduxDispatchProps, SettingsPageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class SettingsPage extends React.Component<ReduxStateProps & ReduxDispatchProps & SettingsPageProps, void | Readonly<{}>> {

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
                </Card.Group>
            </Container>
        );
    }
}