import * as React from 'react';
import {connect, Dispatch} from 'react-redux';

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {Route, RouteComponentProps} from "react-router";
import {InventoryActionRequest, PushActionRequest, ReadActionRequest} from "../actions/devices";
import {MacOSDeviceDetail} from '../components/MacOSDeviceDetail';
import {DeviceState} from "../reducers/device";
import {Link} from "react-router-dom";
import {Container, Grid, Menu, Button, Segment, Dropdown} from 'semantic-ui-react';
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import {SyntheticEvent} from "react";
import {DeviceCertificates} from "./devices/DeviceCertificates";
import {DeviceCommands} from "./devices/DeviceCommands";

interface ReduxStateProps {
    device: DeviceState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        device: state.device
    };
}

interface ReduxDispatchProps {
    read: ReadActionRequest;
    push: PushActionRequest;
    inventory: InventoryActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        read: actions.read,
        push: actions.push,
        inventory: actions.inventory
    }, dispatch);
}

interface RouteParameters {
    id: number;
}

interface DevicePageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteParameters> {
    componentDidMount: () => void;
}

interface DevicePageState {
    filter: string;
}

@connect<ReduxStateProps, ReduxDispatchProps, DevicePageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DevicePage extends React.Component<DevicePageProps, DevicePageState> {

    handleAction = (e: SyntheticEvent<any>, {value}) => {
        e.preventDefault();
        switch (value) {
            case 'push':
                this.props.push(this.props.device.device.id);
                break;
            case 'inventory':
                this.props.inventory(this.props.device.device.id);
                break;
        }
    };

    componentDidMount(): void {
        this.props.read(this.props.match.params.id, []);
    }

    render(): JSX.Element {
        const {
            children,
            device,
            match: {params: {id: device_id}, url}
        } = this.props;

        console.log(url);

        return (
            <Container className='DevicePage'>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Dropdown inline text="action" onChange={this.handleAction} options={[
                                {text: 'Force Push', value: 'push'},
                                {text: 'Inventory', value: 'inventory '}
                            ]}></Dropdown>
                            <Segment>
                                {device && <MacOSDeviceDetail device={device}/>}
                            </Segment>
                            <Menu pointing secondary color="purple" inverted>
                                <MenuItemLink to={`/devices/${device_id}/certificates`} label="Certificates"/>
                                <MenuItemLink to={`/devices/${device_id}/commands`} label="Commands"/>
                            </Menu>
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column>
                            <Route path='/devices/:id/certificates' component={DeviceCertificates}/>
                            <Route path='/devices/:id/commands' component={DeviceCommands}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }
}