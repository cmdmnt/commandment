import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import { Grid, Header, Container } from 'semantic-ui-react'

import {bindActionCreators} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {DevicesState} from "../reducers/devices";
import {IndexActionRequest} from "../actions/devices";
import {ModelIcon} from '../components/griddle/ModelIcon';
import {DeviceLink} from '../components/griddle/DeviceLink';
import {SinceNowUTC} from "../components/griddle/SinceNowUTC";
import {SimpleLayout} from '../components/griddle/SimpleLayout';
import {SelectionPlugin} from '../griddle-plugins/selection';
import {DeviceColumn} from "../components/griddle/DeviceColumn";
import {MultiAttrCellPlugin} from "../griddle-plugins/multiattr-cell/index";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";

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

    handleSort = (sortProperties: { id: string; }) => {
        console.dir(sortProperties);
    };

    handleNextPage = () => {

    };

    handlePrevPage = () => {
        
    };

    handleGetPage = (pageNumber: number) => {
        console.log(pageNumber);
    };

    render(): JSX.Element {
        const {
            devices
        } = this.props;

        const eventHandlers = {
            onFilter: this.handleFilter,
            onSort: this.handleSort,
            onNext: this.handleNextPage,
            onPrev: this.handlePrevPage,
            onGetPage: this.handleGetPage
        };

        return (
            <Container className='DevicesPage'>
                <Grid>
                <Grid.Column>
                <Header as="h1">Devices</Header>

                <Griddle
                    data={devices.items}
                    pageProperties={{
                        currentPage: devices.currentPage,
                        pageSize: devices.pageSize,
                        recordCount: devices.recordCount
                    }}
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table'
                        }
                    }}
                    events={eventHandlers}
                    plugins={[SemanticUIPlugin(), SelectionPlugin(), MultiAttrCellPlugin()]}
                    components={{
                        Layout: SimpleLayout
                    }}
                >
                    <RowDefinition>
                        <ColumnDefinition title='Device' id="id,attributes.model_name,attributes.device_name" customComponent={DeviceColumn} />
                        <ColumnDefinition title='Model' id='attributes.model_name' customComponent={ModelIcon} />
                        <ColumnDefinition title="Name" id="attributes.device_name" />
                        <ColumnDefinition title="Last Seen" id="attributes.last_seen" customComponent={SinceNowUTC} />
                        <ColumnDefinition title="Product Name" id="attributes.product_name" />
                    </RowDefinition>
                </Griddle>
                </Grid.Column>
                </Grid>
            </Container>
        );
    }
}