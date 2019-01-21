import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {AppDeployStatusTable} from "../../components/react-tables/AppDeployStatusTable";
import {RootState} from "../../reducers";
import {devices, DevicesActionRequest, index, IndexActionRequest} from "../../store/applications/managed";
import {IManagedApplicationsState} from "../../store/applications/managed_reducer";
import {FlaskFilterOperation} from "../../flask-rest-jsonapi";
import {IReactTableState} from "../../store/table/types";
import {managed, ManagedActionRequest} from "../../store/applications/actions";
import {FlaskFilter} from "../../flask-rest-jsonapi";

interface IDispatchProps {
    index: IndexActionRequest;
    devices: DevicesActionRequest;
    managed: ManagedActionRequest;
}

interface IStateProps {
    store: IManagedApplicationsState;
}

interface IApplicationDeviceStatusRouteProps {
    id?: string;
}

export type IApplicationDeviceStatusProps = IDispatchProps & IStateProps &
    RouteComponentProps<IApplicationDeviceStatusRouteProps>;

class UnconnectedApplicationDeviceStatus extends React.Component<IApplicationDeviceStatusProps, void> {

    public render() {
        const { store } = this.props;

        return (
            <div className="ApplicationDeviceStatus">
                <AppDeployStatusTable
                    data={store.items}
                    defaultPageSize={store.pageSize}
                    loading={store.loading}
                    onFetchData={this.fetchData}
                    pages={store.pages}
                    />
            </div>
        )
    }

    private fetchData = (state: IReactTableState) => {
        const appId = this.props.match.params.id;
        const sorting = state.sorted.map((value) => (value.desc ? value.id : "-" + value.id));
        const filtering: FlaskFilter[] = state.filtered.map((value) => {
            return {
                name: value.id,
                op: "ilike" as FlaskFilterOperation,
                val: `%25${value.value}%25`,
            };
        });

        this.props.managed(appId, state.pageSize, state.page + 1, sorting, filtering);
    }
}

export const ApplicationDeviceStatus = connect(
    (state: RootState) => ({
        store: state.managed_applications,
}),
    (dispatch: Dispatch) => bindActionCreators({
        devices,
        index,
        managed,
}, dispatch))(UnconnectedApplicationDeviceStatus);
