import * as React from "react";
import {connect} from "react-redux";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators, Dispatch} from "redux";
import {DeviceProfilesTable} from "../../components/react-tables/DeviceProfilesTable";
import {InstalledProfilesState} from "../../store/device/installed_profiles_reducer";
import {RootState} from "../../reducers/index";
import {InstalledProfilesActionRequest, profiles as fetchInstalledProfiles} from "../../store/device/profiles";
import {IReactTableState} from "../../store/table/types";
import {FlaskFilterOperation} from "../../flask-rest-jsonapi";
import {FlaskFilter} from "../../flask-rest-jsonapi";

interface ReduxStateProps {
    profiles?: InstalledProfilesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        profiles: state.device.installed_profiles,
    }
}

interface ReduxDispatchProps {
    fetchInstalledProfiles: InstalledProfilesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch): ReduxDispatchProps {
   return bindActionCreators({
       fetchInstalledProfiles,
   }, dispatch);
}

interface DeviceProfilesRouteProps {
    id?: string;
}

interface DeviceProfilesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceProfilesRouteProps> {

}

class UnconnectedDeviceProfiles extends React.Component<DeviceProfilesProps, undefined> {

    // componentWillMount?() {
    //     this.props.fetchInstalledProfiles(''+this.props.match.params.id, this.props.griddleState.pageSize, 1);
    // }

    public render() {
        const {
            profiles,
        } = this.props;

        return (
            <div className="DeviceProfiles container">
                <DeviceProfilesTable
                    data={profiles.items}
                    defaultPageSize={profiles.pageSize}
                    loading={profiles.loading}
                    onFetchData={this.fetchData}
                    pages={profiles.pages}
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

        this.props.fetchInstalledProfiles(this.props.match.params.id, state.pageSize, state.page + 1, sorting, filtering);
    }
}

export const DeviceProfiles = connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDeviceProfiles);
