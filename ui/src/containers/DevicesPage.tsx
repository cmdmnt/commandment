import * as React from "react";
import {connect, Dispatch} from "react-redux";
import Grid from "semantic-ui-react/src/collections/Grid";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import {RouteComponentProps} from "react-router";
import {bindActionCreators, Store} from "redux";
import {SUISelectionTools} from "../components/react-table/SUISelectionTools";
import {DevicesTable} from "../components/react-tables/DevicesTable";
import {RootState} from "../reducers/index";
import {FlaskFilter, FlaskFilterOperation} from "../store/constants";
import * as actions from "../store/device/actions";
import {DevicesState} from "../store/devices/devices";
import * as tableActions from "../store/table/actions";
import {ToggleSelectionActionCreator} from "../store/table/actions";
import {ITableState} from "../store/table/reducer";
import {IReactTableState} from "../store/table/types";
import * as tagActions from "../store/tags/actions";
import {ITagsState} from "../store/tags/reducer";

interface IReduxStateProps {
    devices: DevicesState;
    table: ITableState;
    tags: ITagsState;
}

function mapStateToProps(state: RootState, ownProps?: any): IReduxStateProps {
    return {
        devices: state.devices,
        table: state.table,
        tags: state.tags,
    };
}

interface IReduxDispatchProps {
    fetchDevicesIfRequired: any;
    index: actions.IndexActionRequest;
    tagIndex: tagActions.IndexActionRequest;
    toggleSelection: ToggleSelectionActionCreator;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps {
    return bindActionCreators({
        fetchDevicesIfRequired: actions.fetchDevicesIfRequired,
        index: actions.index,
        tagIndex: tagActions.index,
        toggleSelection: tableActions.toggleSelection,
    }, dispatch);
}

type DevicesPageProps = IReduxStateProps & IReduxDispatchProps & RouteComponentProps<any>;

class UnconnectedDevicesPage extends React.Component<DevicesPageProps, any> {

    public componentWillMount?(): void {
        // this.props.index();
        this.props.fetchDevicesIfRequired();
        this.props.tagIndex();
    }

    public render(): JSX.Element {
        const {
            devices,
            toggleSelection,
            table,
            tags,
        } = this.props;

        return (
            <Container className="DevicesPage">
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Devices</Header>

                        <SUISelectionTools loading={devices.loading || tags.loading}
                                           tags={tags.items} selectionCount={table.selection.length} />
                        <DevicesTable
                            data={devices.items}
                            loading={devices.loading}
                            toggleSelection={toggleSelection}
                            isSelected={(key) => table.selection.indexOf(key) !== -1}
                            onFetchData={this.fetchData}
                        />
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }

    private fetchData = (state: IReactTableState) => {
        const sorting = state.sorted.map((value) => (value.desc ? value.id : "-" + value.id));
        const filtering: FlaskFilter[] = state.filtered.map((value) => {
            return {
                name: value.id,
                op: "ilike" as FlaskFilterOperation,
                val: `%25${value.value}%25`,
            };
        });

        this.props.index(state.pageSize, state.page, sorting, filtering);
    }
}

export const DevicesPage = connect<IReduxStateProps, IReduxDispatchProps, DevicesPageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDevicesPage);
