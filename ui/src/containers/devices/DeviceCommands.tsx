import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {DeviceCommandsTable} from "../../components/react-tables/DeviceCommandsTable";
import {DeviceCommandsState} from "../../store/device/commands_reducer";
import {RootState} from "../../reducers/index";
import {commands as fetchCommands, CommandsActionRequest} from "../../store/device/actions";
import {IReactTableState} from "../../store/table/types";
import {FlaskFilter, FlaskFilterOperation} from "../../store/constants";

interface IReduxStateProps {
    commands?: DeviceCommandsState;
}

function mapStateToProps(state: RootState, ownProps?: any): IReduxStateProps {
    return {
        commands: state.device.commands,
    }
}

interface IReduxDispatchProps {
    fetchCommands: CommandsActionRequest
}

function mapDispatchToProps(dispatch: Dispatch<any>): IReduxDispatchProps {
   return bindActionCreators({
       fetchCommands,
   }, dispatch);
}

interface IDeviceCommandsRouteProps {
    id: number;
}

type DeviceCommandsProps = IReduxStateProps & IReduxDispatchProps & RouteComponentProps<IDeviceCommandsRouteProps>;

export class UnconnectedDeviceCommands extends React.Component<DeviceCommandsProps, any> {

    // componentWillMount?() {
    //     this.props.fetchCommands(''+this.props.match.params.id, 10, 1, ['-sent_at']);
    // }

    public render() {
        const {
            commands,
        } = this.props;

        return (
            <div className="DeviceCommands container">
                <DeviceCommandsTable
                    data={commands.items}
                    defaultPageSize={commands.pageSize}
                    loading={commands.loading}
                    onFetchData={this.fetchData}
                    pages={commands.pages}
                    defaultSorted={[
                        { id: "sent_at", desc: false },
                    ]}
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

        this.props.fetchCommands(this.props.match.params.id, state.pageSize, state.page + 1, sorting, filtering);
    }
}

export const DeviceCommands = connect<IReduxStateProps, IReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDeviceCommands);
