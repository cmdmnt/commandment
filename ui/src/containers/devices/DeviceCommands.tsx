import * as React from 'react';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {SinceNowUTC} from "../../components/griddle/SinceNowUTC";
import {RootState} from "../../reducers/index";
import {DeviceCommandsState} from "../../reducers/device/commands";
import {connect, Dispatch} from "react-redux";
import {CommandStatus} from "../../components/griddle/CommandStatus";

interface ReduxStateProps {
    commands?: DeviceCommandsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        commands: state.device.commands
    }
}

interface ReduxDispatchProps {

}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
   return {};
}


interface DeviceCommandsProps extends ReduxStateProps, ReduxDispatchProps {

}

@connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps
)
export class DeviceCommands extends React.Component<DeviceCommandsProps, undefined> {
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
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table'
                        }
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
                </div>
            </div>
        )
    }
}
