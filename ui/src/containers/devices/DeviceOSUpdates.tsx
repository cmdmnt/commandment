import * as React from 'react';
import {connect, Dispatch} from "react-redux";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {RootState} from "../../reducers/index";
import {AvailableOSUpdatesState} from "../../reducers/device/available_os_updates";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {AvailableOSUpdatesActionRequest, updates as fetchAvailableOSUpdates} from "../../actions/device/updates";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";



interface ReduxStateProps {
    updates?: AvailableOSUpdatesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        updates: state.device.available_os_updates
    }
}

interface ReduxDispatchProps {
    fetchAvailableOSUpdates: AvailableOSUpdatesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
   return bindActionCreators({
       fetchAvailableOSUpdates
   }, dispatch);
}

interface DeviceOSUpdatesRouteProps {
    id: number;
}

interface DeviceOSUpdatesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceOSUpdatesRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}


class BaseDeviceOSUpdates extends React.Component<DeviceOSUpdatesProps, undefined> {

    componentWillMount?() {
        this.props.fetchAvailableOSUpdates(''+this.props.match.params.id, this.props.griddleState.pageSize, 1);
    }

    componentWillUpdate?(nextProps: DeviceOSUpdatesProps, nextState: void | Readonly<{}>) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter || nextGriddleState.currentPage !== griddleState.currentPage) {
            this.props.fetchAvailableOSUpdates(
                ''+this.props.match.params.id,
                nextGriddleState.pageSize,
                nextGriddleState.currentPage, [],
                [{ name: 'human_readable_name', op: 'ilike', val: `%${nextGriddleState.filter}%` }]);
        }
    }

    render() {
        const {
            updates
        } = this.props;

        return (
            <div className='DeviceOSUpdates container'>

                {updates &&
                <Griddle
                    data={updates.items}
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table',
                            NoResults: 'ui message',
                        }
                    }}
                    events={this.props.events}
                    components={{Layout}}
                    pageProperties={{
                        recordCount: updates.recordCount,
                        currentPage: this.props.griddleState.currentPage,
                        pageSize: this.props.griddleState.pageSize
                    }}
                >
                    <RowDefinition>
                        <ColumnDefinition title='Name' id='attributes.human_readable_name' />
                        <ColumnDefinition title='Version' id="attributes.version" />
                    </RowDefinition>
                </Griddle>}
            </div>
        )
    }
}

export const DeviceOSUpdates = connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps
)(griddle(BaseDeviceOSUpdates));
