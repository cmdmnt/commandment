import * as React from 'react';
import {connect, Dispatch} from "react-redux";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {SinceNowUTC} from "../../components/griddle/SinceNowUTC";
import {IRootState} from "../../reducers/index";
import {InstalledProfilesState} from "../../reducers/device/installed_profiles";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {InstalledProfilesActionRequest, profiles as fetchInstalledProfiles} from "../../actions/device/profiles";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";



interface ReduxStateProps {
    profiles?: InstalledProfilesState;
}

function mapStateToProps(state: IRootState, ownProps?: any): ReduxStateProps {
    return {
        profiles: state.device.installed_profiles
    }
}

interface ReduxDispatchProps {
    fetchInstalledProfiles: InstalledProfilesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
   return bindActionCreators({
       fetchInstalledProfiles
   }, dispatch);
}

interface DeviceProfilesRouteProps {
    id: number;
}

interface DeviceProfilesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceProfilesRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}


class UnconnectedDeviceProfiles extends React.Component<DeviceProfilesProps, undefined> {

    componentWillMount?() {
        this.props.fetchInstalledProfiles(''+this.props.match.params.id, this.props.griddleState.pageSize, 1);
    }

    componentWillUpdate?(nextProps: DeviceProfilesProps, nextState: void | Readonly<{}>) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter || nextGriddleState.currentPage !== griddleState.currentPage) {
            this.props.fetchInstalledProfiles(
                ''+this.props.match.params.id,
                nextGriddleState.pageSize,
                nextGriddleState.currentPage, [],
                [{ name: 'payload_display_name', op: 'ilike', val: `%${nextGriddleState.filter}%` }]);
        }
    }

    render() {
        const {
            profiles
        } = this.props;

        return (
            <div className='DeviceProfiles container'>

                {profiles &&
                <Griddle
                    data={profiles.items}
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
                        recordCount: profiles.recordCount,
                        currentPage: this.props.griddleState.currentPage,
                        pageSize: this.props.griddleState.pageSize
                    }}
                >
                    <RowDefinition>
                        <ColumnDefinition title='Display Name' id='attributes.payload_display_name' />
                        <ColumnDefinition title='Identifier' id="attributes.payload_identifier" />
                    </RowDefinition>
                </Griddle>}
            </div>
        )
    }
}

export const DeviceProfiles = connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps
)(griddle(UnconnectedDeviceProfiles));

