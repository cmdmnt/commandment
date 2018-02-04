import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {Link} from "react-router-dom";
import {bindActionCreators} from "redux";
import {RootState} from "../src/reducers/index";

import Grid from "semantic-ui-react/src/collections/Grid";
import Button from "semantic-ui-react/src/elements/Button";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import {RouteComponentProps} from "react-router";
import {index, IndexActionRequest} from "../src/actions/device_groups";
import {RouteLinkColumn} from "../src/components/griddle/RouteLinkColumn";
import {SimpleLayout} from "../src/components/griddle/SimpleLayout";
import {SelectionPlugin} from "../src/griddle-plugins/selection/index";
import {SemanticUIPlugin} from "../src/griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorState} from "../src/hoc/griddle";
import {DeviceGroupsState} from "../src/reducers/device_groups";

interface ReduxStateProps {
    device_groups: DeviceGroupsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        device_groups: state.device_groups,
    };
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>): ReduxDispatchProps {
    return bindActionCreators({
        index,
    }, dispatch);
}

interface DeviceGroupsPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<void> {
    griddleState: GriddleDecoratorState;
    events: any;
}

interface DeviceGroupsPageState {

}

class UnconnectedDeviceGroupsPage extends React.Component<DeviceGroupsPageProps, DeviceGroupsPageState> {

    componentWillMount?() {
        this.props.index();
    }

    render() {
        const {
            device_groups,
            griddleState,
        } = this.props;

        return (
            <Container className="DeviceGroupsPage">
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Groups</Header>
                        <Button primary as={Link} to="/device_groups/add">New</Button>

                        <Griddle
                            data={device_groups.items}
                            pageProperties={{
                                currentPage: griddleState.currentPage,
                                pageSize: griddleState.pageSize,
                                recordCount: device_groups.recordCount,
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: "ui celled table",
                                    NoResults: "ui message",
                                },
                            }}
                            plugins={[SemanticUIPlugin()]}
                            components={{
                                Layout: SimpleLayout,
                            }}
                        >
                            <RowDefinition onClick={() => console.log("fmeh")}>
                                <ColumnDefinition title="ID" id="id" customComponent={RouteLinkColumn} urlPrefix="/device_groups/" />
                                <ColumnDefinition title="Name" id="attributes.name" />
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
    mapDispatchToProps,
)(griddle(UnconnectedDeviceGroupsPage));
