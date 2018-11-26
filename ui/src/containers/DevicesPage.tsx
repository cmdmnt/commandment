import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import Grid from "semantic-ui-react/src/collections/Grid";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import {components} from "griddle-react";
import {List, Map} from "immutable";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Store} from "redux";
import {IndexActionRequest} from "../store/device/actions";
import * as actions from "../store/device/actions";
import {DeviceColumn} from "../components/griddle/DeviceColumn";
import {DeviceTypeFilter, DeviceTypeFilterValues} from "../components/griddle/DeviceTypeFilter";
import {OSVerColumn} from "../components/griddle/OSVerColumn";
import {SimpleLayout} from "../components/griddle/SimpleLayout";
import {SinceNowUTC} from "../components/griddle/SinceNowUTC";
import {ModelIcon} from "../components/ModelIcon";
import {MultiAttrCellPlugin} from "../griddle-plugins/multiattr-cell/index";
import {SelectionPlugin} from "../griddle-plugins/selection";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorHandlers, GriddleDecoratorState} from "../hoc/griddle";
import {DevicesState} from "../reducers/devices";
import {RootState} from "../reducers/index";

const rowDataSelector = (state: Map<string, any>, { griddleKey }: { griddleKey?: string }) => {
    return state
        .get("data")
        .find((rowMap: any) => rowMap.get("griddleKey") === griddleKey)
        .toJSON();
};

const enhancedWithRowData = connect((state, props: components.RowProps) => {
    return {
        // rowData will be available into MyCustomComponent
        rowData: rowDataSelector(state, props),
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
        fetchDevicesIfRequired: actions.fetchDevicesIfRequired,
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

    handleDeviceTypeFilterChange = (selected: DeviceTypeFilterValues) => {
        // console.log(selected);
    };

    render(): JSX.Element {
        const {
            griddleState,
            devices,
        } = this.props;

        return (
            <Container className="DevicesPage">
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Devices</Header>
                        {/*<DeviceTypeFilter onClick={this.handleDeviceTypeFilterChange} selected={'all'} />*/}
                        <Griddle
                            data={devices.items}
                            pageProperties={{
                                currentPage: griddleState.currentPage,
                                pageSize: griddleState.pageSize,
                                recordCount: devices.recordCount,
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: "ui celled table",
                                },
                            }}
                            events={this.props.events}
                            plugins={[SemanticUIPlugin(), SelectionPlugin()]}
                            components={{
                                Layout: SimpleLayout,
                            }}
                        >
                            <RowDefinition onClick={() => console.log("fmeh")}>
                                <ColumnDefinition title="Type" id="attributes.model_name"
                                                  customComponent={ModelIcon} width={60} style={{textAlign: "center"}} />
                                <ColumnDefinition title="Name" id="id,attributes.model_name,attributes.device_name"
                                                  customComponent={enhancedWithRowData(DeviceColumn)}/>
                                <ColumnDefinition title="Serial" id="attributes.serial_number"
                                                   width={140} />
                                <ColumnDefinition title="OS" id="attributes.model_name,attributes.os_version"
                                                  customComponent={enhancedWithRowData(OSVerColumn)}/>
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
    mapDispatchToProps,
)(griddle(UnconnectedDevicesPage));
