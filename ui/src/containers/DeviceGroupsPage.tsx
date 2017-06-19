import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RootState} from "../reducers/index";
import {bindActionCreators} from "redux";
import {Link} from 'react-router-dom';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {Grid, Header, Container, Button} from 'semantic-ui-react'
import {SelectionPlugin} from '../griddle-plugins/selection';
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";
import {SimpleLayout} from "../components/griddle/SimpleLayout";
import {DeviceGroupsState} from "../reducers/device_groups";
import {index, IndexActionRequest} from '../actions/device_groups';
import {griddle, GriddleDecoratorState} from "../hoc/griddle";
import {RouteLinkColumn} from "../components/griddle/RouteLinkColumn";

interface ReduxStateProps {
    device_groups: DeviceGroupsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        device_groups: state.device_groups
    };
}


interface ReduxDispatchProps {
    index: IndexActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>): ReduxDispatchProps {
    return bindActionCreators({
        index
    }, dispatch);
}

interface DeviceGroupsPageProps extends ReduxStateProps, ReduxDispatchProps {
    griddleState: GriddleDecoratorState;
    events: any;
}

interface DeviceGroupsPageState {
    
}

@griddle
class BaseDeviceGroupsPage extends React.Component<DeviceGroupsPageProps, DeviceGroupsPageState> {

    componentWillMount?() {
        this.props.index();
    }

    render() {
        const {
            device_groups,
            griddleState
        } = this.props;

        return (
            <Container className='DeviceGroupsPage'>
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Groups</Header>
                        <Button primary as={Link} to='/device_groups/add'>New</Button>

                        <Griddle
                            data={device_groups.items}
                            pageProperties={{
                                currentPage: griddleState.currentPage,
                                pageSize: griddleState.pageSize,
                                recordCount: device_groups.recordCount
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: 'ui celled table',
                                    NoResults: 'ui message'
                                }
                            }}
                            plugins={[SemanticUIPlugin()]}
                            components={{
                                Layout: SimpleLayout
                            }}
                        >
                            <RowDefinition onClick={() => console.log('fmeh')}>
                                <ColumnDefinition title='ID' id='id' customComponent={RouteLinkColumn} urlPrefix='/device_groups/' />
                                <ColumnDefinition title='Name' id='attributes.name' />
                            </RowDefinition>
                        </Griddle>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}

export const DeviceGroupsPage = connect<ReduxStateProps, ReduxDispatchProps, DeviceGroupsPageProps>(
    mapStateToProps,
    mapDispatchToProps
)(BaseDeviceGroupsPage);