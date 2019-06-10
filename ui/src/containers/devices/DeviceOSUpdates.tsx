import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {FlaskFilter, FlaskFilters} from "../../flask-rest-jsonapi";
import {DeviceUpdatesTable} from "../../components/react-tables/DeviceUpdatesTable";
import {RootState} from "../../reducers";
import {AvailableOSUpdatesState} from "../../store/device/available_os_updates_reducer";
import {AvailableOSUpdatesActionRequest, updates as fetchAvailableOSUpdates} from "../../store/device/updates";

import {
    Button,
    Divider,
    Checkbox,
} from "semantic-ui-react";

import {IReactTableState} from "../../store/table/types";
import {FlaskFilterOperation} from "../../flask-rest-jsonapi";

interface IReduxStateProps {
    is_supervised?: boolean;
    updates?: AvailableOSUpdatesState;
}

function mapStateToProps(state: RootState, ownProps?: any): IReduxStateProps {
    return {
        is_supervised: state.device.device.attributes.is_supervised,
        updates: state.device.available_os_updates,
    };
}

interface IReduxDispatchProps {
    fetchAvailableOSUpdates: AvailableOSUpdatesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch): IReduxDispatchProps {
   return bindActionCreators({
       fetchAvailableOSUpdates,
   }, dispatch);
}

interface IDeviceOSUpdatesRouteProps {
    id?: string;
}

interface IDeviceOSUpdatesProps extends IReduxStateProps, IReduxDispatchProps,
    RouteComponentProps<IDeviceOSUpdatesRouteProps> {

}

interface IBaseDeviceOSUpdatesState {
    hide_config_updates: boolean;
}

class BaseDeviceOSUpdates extends React.Component<IDeviceOSUpdatesProps, IBaseDeviceOSUpdatesState> {

    public state: IBaseDeviceOSUpdatesState = {
      hide_config_updates: true,
    };

    // public componentWillMount?() {
    //     const filters: FlaskFilters = [
    //         { name: "is_config_data_update", op: "ne", val: "1" },
    //     ];
    //
    //     this.props.fetchAvailableOSUpdates("" + this.props.match.params.id,
    //         this.props.griddleState.pageSize, 1, [], filters);
    // }

    public render() {
        const {
            updates,
            is_supervised,
        } = this.props;

        return (
            <div className="DeviceOSUpdates container">
                <Checkbox label="Hide configuration data updates (XProtect, Gatekeeper)"
                          checked={this.state.hide_config_updates}
                          onChange={(e) => this.setState({ hide_config_updates: !this.state.hide_config_updates })}
                />
                {is_supervised ?
                    <Button size="small" floated="right">Update All</Button> :
                    <Button size="small" title="Unsupervised" floated="right" disabled>Update All</Button> }
                <Divider/>
                <DeviceUpdatesTable
                    data={updates.items}
                    defaultPageSize={updates.pageSize}
                    loading={updates.loading}
                    onFetchData={this.fetchData}
                    pages={updates.pages}
                />
            </div>
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

        this.props.fetchAvailableOSUpdates(this.props.match.params.id, state.pageSize, state.page + 1, sorting, filtering);
    }
}

export const DeviceOSUpdates = connect<IReduxStateProps, IReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps,
)(BaseDeviceOSUpdates);
