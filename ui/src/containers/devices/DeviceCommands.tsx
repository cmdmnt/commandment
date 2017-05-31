import * as React from 'react';
import {connect, Dispatch} from "react-redux";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {SinceNowUTC} from "../../components/griddle/SinceNowUTC";
import {RootState} from "../../reducers/index";
import {DeviceCommandsState} from "../../reducers/device/commands";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {CommandsActionRequest, commands as fetchCommands} from "../../actions/devices";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";



interface ReduxStateProps {
    commands?: DeviceCommandsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        commands: state.device.commands
    }
}

interface ReduxDispatchProps {
    fetchCommands: CommandsActionRequest
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
   return bindActionCreators({
       fetchCommands
   }, dispatch);
}

interface DeviceCommandsRouteProps {
    id: number;
}

interface DeviceCommandsProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceCommandsRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}


@connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps
)
@griddle
export class DeviceCommands extends React.Component<DeviceCommandsProps, undefined> {

    componentWillMount?() {
        this.props.fetchCommands(this.props.match.params.id, 10, 1, ['-sent_at']);
    }

    componentWillUpdate?(nextProps: DeviceCommandsProps, nextState: void | Readonly<DeviceCommandsState>) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter || nextGriddleState.currentPage !== griddleState.currentPage) {
            this.props.fetchCommands(
                this.props.match.params.id,
                10, nextGriddleState.currentPage, [], []);
        }
    }

    render() {
        const {
            commands
        } = this.props;

        return (
            <div className='DeviceCommands container'>

                {commands &&
                <Griddle
                    data={commands.items}
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table',
                            NoResults: 'ui message'
                        }
                    }}
                    events={this.props.events}
                    components={{Layout}}
                    pageProperties={{
                        recordCount: commands.recordCount,
                        currentPage: this.props.griddleState.currentPage,
                        pageSize: this.props.griddleState.pageSize
                    }}
                >
                    <RowDefinition>
                        <ColumnDefinition id="id" />
                        <ColumnDefinition title='Type' id='attributes.request_type' />
                        <ColumnDefinition title='Status' id="attributes.status" />
                        <ColumnDefinition title='Sent' id="attributes.sent_at" customComponent={SinceNowUTC} />
                    </RowDefinition>
                </Griddle>}
            </div>
        )
    }
}
