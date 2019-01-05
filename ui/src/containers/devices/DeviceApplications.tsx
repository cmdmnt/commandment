import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {DeviceApplicationsTable} from "../../components/react-tables/DeviceApplicationsTable";
import {RootState} from "../../reducers/index";
import {FlaskFilter, FlaskFilterOperation} from "../../store/constants";
import {
    applications as fetchInstalledApplications, InstalledApplicationsActionRequest,
} from "../../store/device/applications";
import {InstalledApplicationsState} from "../../store/device/installed_applications_reducer";
import {IReactTableState} from "../../store/table/types";

interface IReduxStateProps {
    installed_applications?: InstalledApplicationsState;
}

function mapStateToProps(state: RootState, ownProps?: any): IReduxStateProps {
    return {
        installed_applications: state.device.installed_applications,
    }
}

interface IReduxDispatchProps {
    fetchInstalledApplications: InstalledApplicationsActionRequest
}

function mapDispatchToProps(dispatch: Dispatch): IReduxDispatchProps {
   return bindActionCreators({
       fetchInstalledApplications,
   }, dispatch);
}

interface IDeviceApplicationsRouteProps {
    id?: string;
}

type DeviceApplicationsProps = IReduxStateProps &
    IReduxDispatchProps &
    RouteComponentProps<IDeviceApplicationsRouteProps>;

export class UnconnectedDeviceApplications extends React.Component<DeviceApplicationsProps, undefined> {
    public render() {
        const {
            installed_applications,
        } = this.props;

        return (
            <div className="DeviceApplications container">
                {installed_applications.items &&
                <DeviceApplicationsTable
                  data={installed_applications.items}
                  defaultPageSize={installed_applications.pageSize}
                  loading={installed_applications.loading}
                  onFetchData={this.fetchData}
                  pages={installed_applications.pages}
                  defaultSorted={[
                      { id: "name", desc: true },
                  ]}
                />}
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

        this.props.fetchInstalledApplications(this.props.match.params.id, state.pageSize, state.page + 1, sorting, filtering);
    }
}

export const DeviceApplications = connect<IReduxStateProps, IReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDeviceApplications);
