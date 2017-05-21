import * as React from 'react';
import {connect, Dispatch} from "react-redux";
import Griddle, {RowDefinition, ColumnDefinition, SortProperties} from 'griddle-react';
import {SinceNowUTC} from "../../components/griddle/SinceNowUTC";
import {RootState} from "../../reducers/index";
import {DeviceCommandsState} from "../../reducers/device/commands";
import {SUIFilter as Filter} from "../../components/griddle/SUIFilter";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {SUIPagination as Pagination} from '../../components/griddle/SUIPagination';
import {SUIPageList as PageDropdown} from '../../components/griddle/SUIPageList';
import {SUINextButton as NextButton} from '../../components/griddle/SUINextButton';
import {SUIPrevButton as PrevButton} from '../../components/griddle/SUIPrevButton';
import {CommandStatus} from "../../components/griddle/CommandStatus";
import {CommandsActionRequest, commands as fetchCommands} from "../../actions/devices";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";



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
                    components={{ Filter, Layout, NextButton, PrevButton, PageDropdown, Pagination }}
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
