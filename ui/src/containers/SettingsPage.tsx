import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {bindActionCreators} from 'redux';
import {RootState} from "../reducers/index";
import { Container, Card } from 'semantic-ui-react'

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

interface SettingsPageProps extends ReduxStateProps, ReduxDispatchProps {

}

@connect<ReduxStateProps, ReduxDispatchProps, SettingsPageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class SettingsPage extends React.Component<SettingsPageProps, undefined> {

    render() {
        const {

        } = this.props;

        return (
            <Container>
                <Card.Group>
                    <Card
                        header='Organization'
                        description='Configure your organization'
                    />
                </Card.Group>
                <Card.Group>
                    <Card
                        header='SCEP'
                        description='Configure scep'
                    />
                </Card.Group>
            </Container>
        );
    }
}