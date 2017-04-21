import * as React from 'react';
import {connect, Dispatch} from 'react-redux';

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {InventoryActionRequest, PushActionRequest, ReadActionRequest} from "../actions/devices";
import {MacOSDeviceDetail} from '../components/MacOSDeviceDetail';
import {DeviceState} from "../reducers/device";

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
        this.props.read(this.props.match.params.id, ['commands']);
    }

    render(): JSX.Element {
        const {
            device
        } = this.props;

        return (
            <div className='DevicePage top-margin container'>
                <button className='button button-outline' onClick={this.handlePush}>Force Push</button>
                <button className='button button-outline' onClick={this.handleInventory}>Inventory</button>
                {device && <MacOSDeviceDetail device={device} />}
            </div>
        );
    }
}