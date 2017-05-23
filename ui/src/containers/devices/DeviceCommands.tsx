import * as React from 'react';
import {connect, Dispatch} from "react-redux";
import Griddle, {RowDefinition, ColumnDefinition, SortProperties} from 'griddle-react';
import {SinceNowUTC} from "../../components/griddle/SinceNowUTC";
import {RootState} from "../../reducers/index";
import {DeviceCommandsState} from "../../reducers/device/commands";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {CommandStatus} from "../../components/griddle/CommandStatus";
import {CommandsActionRequest, commands as fetchCommands} from "../../actions/devices";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";



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

}

@connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps
)
export class DeviceCommands extends React.Component<DeviceCommandsProps, undefined> {

    onSort = (sortProperties: SortProperties) => {
        console.log(sortProperties);
    };

    componentWillMount() {
        this.props.fetchCommands(this.props.match.params.id);
    }

    render() {
        const {
            commands
        } = this.props;

        return (
            <div className='DeviceCommands container'>
                <div className='row'>
                    <div className='column'>
                {commands &&
                <Griddle
                    data={commands.items}
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table'
                        }
                    }}
                    events={{
                        onSort: this.onSort
                    }}
                    pageProperties={commands.pageProperties}
                >
                    <RowDefinition>
                        <ColumnDefinition id="id" />
                        <ColumnDefinition title='Type' id='attributes.request_type' />
                        <ColumnDefinition title='Status' id="attributes.status" />
                        <ColumnDefinition title='Sent' id="attributes.sent_at" customComponent={SinceNowUTC} />
                    </RowDefinition>
                </Griddle>}
                    </div>
                </div>
            </div>
        )
    }
}
