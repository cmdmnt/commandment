import * as React from 'react';
import {connect, Dispatch} from 'react-redux';

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {InventoryActionRequest, PushActionRequest, ReadActionRequest} from "../actions/devices";
import {MacOSDeviceDetail} from '../components/MacOSDeviceDetail';
import {DeviceState} from "../reducers/device";
import {Link} from "react-router-dom";
import {Container, Grid, Menu, Button} from 'semantic-ui-react';

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

    handlePush = (e: any) => {
        this.props.push(this.props.device.device.id);
    };

    handleInventory = (e: any) => {
        e.preventDefault();
        this.props.inventory(this.props.device.device.id);
    };

    componentDidMount(): void {
        this.props.read(this.props.match.params.id, [
            'commands'
        ]);
    }

    render(): JSX.Element {
        const {
            device,
            match: { params: { id: device_id }}
        } = this.props;

        return (
            <Container className='DevicePage'>
                <Grid>
                    <Grid.Column>
                <Button onClick={this.handlePush}>Force Push</Button>
                <Button onClick={this.handleInventory}>Inventory</Button>

                {device && <MacOSDeviceDetail device={device} />}
                        <Menu secondary>
                            <Menu.Item><Link to={`/devices/${device_id}/certificates`}>Certificates</Link></Menu.Item>
                            <Menu.Item><Link to={`/devices/${device_id}/commands`}>Commands</Link></Menu.Item>
                        </Menu>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}