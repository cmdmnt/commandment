import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {AvailableOSUpdatesActionRequest, updates as fetchAvailableOSUpdates} from "../../store/device/updates";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";
import {RootState} from "../../reducers";
import {AvailableOSUpdatesState} from "../../reducers/device/available_os_updates";
import Button from "semantic-ui-react/dist/commonjs/elements/Button/Button";
import Checkbox from "semantic-ui-react/dist/commonjs/modules/Checkbox/Checkbox";
import {FlaskFilters} from "../../actions/constants";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

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

function mapDispatchToProps(dispatch: Dispatch<any>): IReduxDispatchProps {
   return bindActionCreators({
       fetchAvailableOSUpdates,
   }, dispatch);
}

interface IDeviceOSUpdatesRouteProps {
    id: number;
}

interface IDeviceOSUpdatesProps extends IReduxStateProps, IReduxDispatchProps,
    RouteComponentProps<IDeviceOSUpdatesRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}

interface IBaseDeviceOSUpdatesState {
    hide_config_updates: boolean;
}

class BaseDeviceOSUpdates extends React.Component<IDeviceOSUpdatesProps, IBaseDeviceOSUpdatesState> {

    public state: IBaseDeviceOSUpdatesState = {
      hide_config_updates: true,
    };

    public componentWillMount?() {
        const filters: FlaskFilters = [
            { name: "is_config_data_update", op: "ne", val: "1" },
        ];

        this.props.fetchAvailableOSUpdates("" + this.props.match.params.id,
            this.props.griddleState.pageSize, 1, [], filters);
    }

    public componentWillUpdate?(nextProps: IDeviceOSUpdatesProps, nextState: IBaseDeviceOSUpdatesState) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter ||
            nextGriddleState.currentPage !== griddleState.currentPage ||
            this.state !== nextState
        ) {
            const filters: FlaskFilters = [{ name: "human_readable_name", op: "ilike", val: `%${nextGriddleState.filter}%` }];
            if (nextState.hide_config_updates) {
                filters.push({ name: "is_config_data_update", op: "ne", val: "1" });
            }

            this.props.fetchAvailableOSUpdates(
                "" + this.props.match.params.id,
                nextGriddleState.pageSize,
                nextGriddleState.currentPage, [],
                filters);
        }
    }

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
                {updates &&
                <Griddle
                    data={updates.items}
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            NoResults: "ui message",
                            Table: "ui celled table",
                        },
                    }}
                    events={this.props.events}
                    components={{Layout}}
                    pageProperties={{
                        currentPage: this.props.griddleState.currentPage,
                        pageSize: this.props.griddleState.pageSize,
                        recordCount: updates.recordCount,
                    }}
                >
                    <RowDefinition>
                        <ColumnDefinition title="Product ID" id="attributes.product_key" />
                        <ColumnDefinition title="Name" id="attributes.human_readable_name" />
                        <ColumnDefinition title="Version" id="attributes.version" />
                    </RowDefinition>
                </Griddle>}
            </div>
        );
    }
}

export const DeviceOSUpdates = connect<IReduxStateProps, IReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps,
)(griddle(BaseDeviceOSUpdates));
