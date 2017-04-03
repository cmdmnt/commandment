import * as React from 'react';
import {connect, Dispatch} from 'react-redux';

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {ReadActionRequest} from "../actions/devices";
import {MacOSDeviceDetail} from '../components/MacOSDeviceDetail';
import {DeviceState} from "../reducers/device";

interface ReduxStateProps {
    device: DeviceState;
}

interface ReduxDispatchProps {
    read: ReadActionRequest;
}

interface RouteParameters {
    id: number;
}

interface DevicePageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteParameters> {
}

interface DevicePageState {
    filter: string;
}

@connect<ReduxStateProps, ReduxDispatchProps, DevicePageProps>(
    (state: RootState, ownProps?: any): ReduxStateProps => {
        return { device: state.device };
    },
    (dispatch: Dispatch<any>): ReduxDispatchProps => {
        return bindActionCreators({
            read: actions.read
        }, dispatch);
    }
)
export class DevicePage extends React.Component<DevicePageProps, DevicePageState> {

    componentDidMount(): void {
        this.props.read(this.props.match.params.id, ['commands']);
    }

    render(): JSX.Element {
        const {
            device
        } = this.props;

        return (
            <div className='DevicePage top-margin container'>
                {device && <MacOSDeviceDetail device={device} />}
            </div>
        );
    }
}