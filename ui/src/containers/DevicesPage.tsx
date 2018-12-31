import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import Grid from "semantic-ui-react/src/collections/Grid";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import {RouteComponentProps} from "react-router";
import {bindActionCreators, Store} from "redux";
import {IndexActionRequest} from "../store/device/actions";
import * as actions from "../store/device/actions";
import * as tableActions from "../store/table/actions";
import {DeviceTypeFilter, DeviceTypeFilterValues} from "../components/griddle/DeviceTypeFilter";
import {griddle, GriddleDecoratorHandlers, GriddleDecoratorState} from "../hoc/griddle";
import {DevicesState} from "../store/devices/devices";
import {RootState} from "../reducers/index";
import {DevicesTable} from "../components/react-tables/DevicesTable";
import {ToggleSelectionActionCreator} from "../store/table/actions";
import {ITableState} from "../store/table/reducer";
import {IReactTableState} from "../store/table/types";
import {FlaskFilter, FlaskFilterOperation} from "../store/constants";

interface ReduxStateProps {
    devices: DevicesState;
    table: ITableState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        devices: state.devices,
        table: state.table,
    };
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
    fetchDevicesIfRequired: any;
    toggleSelection: ToggleSelectionActionCreator;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: any): ReduxDispatchProps {
    return bindActionCreators({
        fetchDevicesIfRequired: actions.fetchDevicesIfRequired,
        index: actions.index,
        toggleSelection: tableActions.toggleSelection,
    }, dispatch);
}

interface DevicesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
}

interface DevicesPageState {
    filter: string;
}

class UnconnectedDevicesPage extends React.Component<DevicesPageProps, DevicesPageState> {

    public componentWillMount?(): void {
        // this.props.index();
        this.props.fetchDevicesIfRequired();
    }

    handleDeviceTypeFilterChange = (selected: DeviceTypeFilterValues) => {
        // console.log(selected);
    };

    public render(): JSX.Element {
        const {
            devices,
            toggleSelection,
            table,
        } = this.props;

        return (
            <Container className="DevicesPage">
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Devices</Header>
                        <DevicesTable
                            data={devices.items}
                            loading={devices.loading}
                            toggleSelection={toggleSelection}
                            isSelected={(key) => table.selection.indexOf(key) !== -1}
                            onFetchData={this.fetchData}
                        />
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }

    private fetchData = (state: IReactTableState) => {
        const sorting = state.sorted.map((value) => (value.desc ? value.id : "-" + value.id));
        const filtering: FlaskFilter[] = state.filtered.map((value) => {
            return {
                name: value.id,
                op: "ilike" as FlaskFilterOperation,
                val: `%25${value.value}%25`,
            };
        });

        this.props.index(state.pageSize, state.page, sorting, filtering);
    }
}

export const DevicesPage = connect<ReduxStateProps, ReduxDispatchProps, DevicesPageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDevicesPage);
