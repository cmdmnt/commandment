import * as React from 'react';
import {connect, Dispatch} from "react-redux";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {SinceNowUTC} from "../../components/griddle/SinceNowUTC";
import {RootState} from "../../reducers/index";
import {InstalledApplicationsState} from "../../reducers/device/installed_applications";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {InstalledApplicationsActionRequest, applications as fetchInstalledApplications} from "../../actions/device/applications";
import {RouteComponentProps, RouteProps} from "react-router";
import {bindActionCreators} from "redux";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";



interface ReduxStateProps {
    applications?: InstalledApplicationsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        applications: state.device.installed_applications
    }
}

interface ReduxDispatchProps {
    fetchInstalledApplications: InstalledApplicationsActionRequest
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
   return bindActionCreators({
       fetchInstalledApplications
   }, dispatch);
}

interface DeviceApplicationsRouteProps {
    id: number;
}

interface DeviceApplicationsProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceApplicationsRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}


@connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps
)
@griddle
export class DeviceApplications extends React.Component<DeviceApplicationsProps, undefined> {

    componentWillMount?() {
        this.props.fetchInstalledApplications(this.props.match.params.id, this.props.griddleState.pageSize, 1);
    }

    componentWillUpdate?(nextProps: DeviceApplicationsProps, nextState: void | Readonly<{}>) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter || nextGriddleState.currentPage !== griddleState.currentPage) {
            this.props.fetchInstalledApplications(
                this.props.match.params.id,
                nextGriddleState.pageSize,
                nextGriddleState.currentPage, [],
                [{ name: 'name', op: 'ilike', val: `%${nextGriddleState.filter}%` }]);
        }
    }

    render() {
        const {
            applications
        } = this.props;

        return (
            <div className='DeviceApplications container'>

                {applications &&
                <Griddle
                    data={applications.items}
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
                        recordCount: applications.recordCount,
                        currentPage: this.props.griddleState.currentPage,
                        pageSize: this.props.griddleState.pageSize
                    }}
                >
                    <RowDefinition>
                        <ColumnDefinition title='Name' id='attributes.name' />
                        <ColumnDefinition title='Version' id="attributes.version" />
                    </RowDefinition>
                </Griddle>}
            </div>
        )
    }
}
