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
import {Container, Grid, Menu, Button, Segment, Dropdown} from 'semantic-ui-react';
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";

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
            match: { params: { id: device_id }, url}
        } = this.props;

        console.log(url);

        return (
            <Container className='DevicePage'>
                <Grid>
                    <Grid.Column>
                        <Dropdown inline options={[
                            { text: 'Force Push', value: 'push' },
                            { text: 'Inventory', value: 'inventory '}
                        ]}></Dropdown>
                        <Segment>
                {device && <MacOSDeviceDetail device={device} />}
                        </Segment>
                        <Menu pointing secondary color="purple" inverted>
                            <MenuItemLink to={`/devices/${device_id}/certificates`} label="Certificates" />
                            <MenuItemLink to={`/devices/${device_id}/commands`} label="Commands" />
                        </Menu>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}