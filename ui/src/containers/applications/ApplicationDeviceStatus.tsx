import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {AppDeployStatusTable} from "../../components/react-tables/AppDeployStatusTable";
import {RootState} from "../../reducers";
import {index, IndexActionRequest} from "../../store/applications/managed";
import {IManagedApplicationsState} from "../../store/applications/managed_reducer";
import {FlaskFilter, FlaskFilterOperation} from "../../store/constants";
import {IReactTableState} from "../../store/table/types";

interface IDispatchProps {
    index: IndexActionRequest;
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
        const sorting = state.sorted.map((value) => (value.desc ? value.id : "-" + value.id));
        const filtering: FlaskFilter[] = state.filtered.map((value) => {
            return {
                name: value.id,
                op: "ilike" as FlaskFilterOperation,
                val: `%25${value.value}%25`,
            };
        });

        this.props.index(state.pageSize, state.page + 1, sorting, filtering, ["device"]);
    }
}

export const ApplicationDeviceStatus = connect(
    (state: RootState) => ({
        store: state.managed_applications,
}),
    (dispatch: Dispatch) => bindActionCreators({
    index,
}, dispatch))(UnconnectedApplicationDeviceStatus);
