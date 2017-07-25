import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {Grid, Header, Container} from 'semantic-ui-react'

import {bindActionCreators, Store} from "redux";
import * as actions from '../actions/devices';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {DevicesState} from "../reducers/devices";
import {IndexActionRequest} from "../actions/devices";
import {SinceNowUTC} from "../components/griddle/SinceNowUTC";
import {SimpleLayout} from '../components/griddle/SimpleLayout';
import {SelectionPlugin} from '../griddle-plugins/selection';
import {DeviceColumn} from "../components/griddle/DeviceColumn";
import {MultiAttrCellPlugin} from "../griddle-plugins/multiattr-cell/index";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorHandlers, GriddleDecoratorState} from "../hoc/griddle";
import {components} from "griddle-react";


const rowDataSelector = (state: any, { griddleKey }: { griddleKey: string }) => {
    return state
        .get('data')
        .find(rowMap => rowMap.get('griddleKey') === griddleKey)
        .toJSON();
};

const enhancedWithRowData = connect((state, props) => {
    return {
        // rowData will be available into MyCustomComponent
        rowData: rowDataSelector(state, props)
    };
});

interface OwnProps {
    
}

interface ReduxStateProps {
    devices: DevicesState;
}

function mapStateToProps(state: RootState, ownProps?: OwnProps): ReduxStateProps {
    return {devices: state.devices};
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
    fetchDevicesIfRequired: any;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: OwnProps): ReduxDispatchProps {
    return bindActionCreators({
        index: actions.index,
        fetchDevicesIfRequired: actions.fetchDevicesIfRequired
    }, dispatch);
}

interface DevicesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
    griddleState: GriddleDecoratorState;
    events: GriddleDecoratorHandlers;
}

interface DevicesPageState {
    filter: string;
}


class UnconnectedDevicesPage extends React.Component<DevicesPageProps, DevicesPageState> {

    componentWillMount?(): void {
        // this.props.index();
        this.props.fetchDevicesIfRequired();
    }

    render(): JSX.Element {
        const {
            griddleState,
            devices
        } = this.props;

        return (
            <Container className='DevicesPage'>
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Devices</Header>

                        <Griddle
                            data={devices.items}
                            pageProperties={{
                                currentPage: griddleState.currentPage,
                                pageSize: griddleState.pageSize,
                                recordCount: devices.recordCount
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: 'ui celled table'
                                }
                            }}
                            events={this.props.events}
                            plugins={[SemanticUIPlugin(), SelectionPlugin()]}
                            components={{
                                Layout: SimpleLayout
                            }}
                        >
                            <RowDefinition onClick={() => console.log('fmeh')}>
                                <ColumnDefinition title='Device' id="id,attributes.model_name,attributes.device_name"
                                                  customComponent={enhancedWithRowData(DeviceColumn)}/>

                                <ColumnDefinition title="Last Seen" id="attributes.last_seen"
                                                  customComponent={SinceNowUTC}/>
                            </RowDefinition>
                        </Griddle>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}

export const DevicesPage = connect<ReduxStateProps, ReduxDispatchProps, DevicesPageProps>(
    mapStateToProps,
    mapDispatchToProps
)(griddle(UnconnectedDevicesPage));