import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {DevicesState} from "../reducers/devices";
import {IndexActionRequest} from "../actions/devices";
import {ModelIcon} from '../components/griddle/ModelIcon';
import {DeviceLink} from '../components/griddle/DeviceLink';
import {SinceNowUTC} from "../components/griddle/SinceNowUTC";

interface ReduxStateProps {
    devices: DevicesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return { devices: state.devices };
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        index: actions.index
    }, dispatch);
}

interface DevicesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
    componentWillMount: () => void;
}

interface DevicesPageState {
    filter: string;
}

@connect<ReduxStateProps, ReduxDispatchProps, DevicesPageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DevicesPage extends React.Component<DevicesPageProps, DevicesPageState> {

    componentWillMount(): void {
        this.props.index();
    }

    handleFilter = (filterText: string) => {
        // TODO: debounce filter text
    };

    render(): JSX.Element {
        const {
            devices
        } = this.props;

        const eventHandlers = {
            onFilter: this.handleFilter,
        };

        return (
            <div className='DevicesPage top-margin container'>
                <div className='row'>
                    <div className='column'>
                        <h1>Devices</h1>
                    </div>
                </div>
                <div className='row'>
                    <div className='column'>
                        <Griddle
                            data={devices.items}
                            pageProperties={{
                                currentPage: devices.currentPage,
                                pageSize: devices.pageSize,
                                recordCount: devices.recordCount
                            }}
                            events={eventHandlers}
                        >
                            <RowDefinition>
                                <ColumnDefinition id="id" customComponent={DeviceLink} />
                                <ColumnDefinition title="Last Seen" id="attributes.last_seen" customComponent={SinceNowUTC} />
                                <ColumnDefinition title="Name" id="attributes.device_name" />
                                <ColumnDefinition title="Product Name" id="attributes.product_name" />
                                <ColumnDefinition title='model' id='attributes.model_name' customComponent={ModelIcon} />
                            </RowDefinition>
                        </Griddle>
                    </div>
                </div>
            </div>
        );
    }
}