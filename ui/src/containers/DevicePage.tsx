import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {ReadActionRequest} from "../actions/devices";

interface ReduxStateProps {
    device: JSONAPIObject<Device>;
}

interface ReduxDispatchProps {
    read: ReadActionRequest;
}

interface RouteParameters {
    id: number;
}

interface DevicePageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteParameters> {
    componentWillMount: () => void;
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
        this.props.read(this.props.match.params.id);
    }

    render(): JSX.Element {
        const {
            device
        } = this.props;

        return (
            <div className='DevicePage top-margin container'>
                READ
            </div>
        );
    }
}