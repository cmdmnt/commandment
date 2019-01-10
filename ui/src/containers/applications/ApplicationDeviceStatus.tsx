import * as React from "react";
import {RouteComponentProps} from "react-router";
import {connect} from "react-redux";
import {RootState} from "../../reducers";
import {bindActionCreators, Dispatch} from "redux";

interface IDispatchProps {

}

interface IStateProps {

}

interface IApplicationDeviceStatusRouteProps {
    id?: string;
}

export type IApplicationDeviceStatusProps = IDispatchProps & IStateProps &
    RouteComponentProps<IApplicationDeviceStatusRouteProps>;

class UnconnectedApplicationDeviceStatus extends React.Component<IApplicationDeviceStatusProps, void> {

    public render() {
        return (
            <div>deployment status</div>
        )
    }
}

export const ApplicationDeviceStatus = connect(
    (state: RootState) => ({

}),
    (dispatch: Dispatch) => bindActionCreators({

}, dispatch))(UnconnectedApplicationDeviceStatus);
