import * as React from "react";
import {connect, Dispatch} from "react-redux";

import Grid from "semantic-ui-react/src/collections/Grid";
import Message from "semantic-ui-react/src/collections/Message";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import * as Dropzone from "react-dropzone";

import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import * as actions from "../actions/profiles";
import {IndexActionRequest, UploadActionRequest} from "../actions/profiles";
import {PayloadScopeIcon} from "../components/griddle/PayloadScopeIcon";
import {RouteLinkColumn} from "../components/griddle/RouteLinkColumn";
import {SimpleLayout as Layout} from "../components/griddle/SimpleLayout";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorHandlers, GriddleDecoratorState} from "../hoc/griddle";
import {RootState} from "../reducers/index";
import {ProfilesState} from "../reducers/profiles";

interface ReduxStateProps {
    profiles: ProfilesState;
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
    upload: UploadActionRequest;
}

interface ProfilesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
    componentWillMount: () => void;
    griddleState: GriddleDecoratorState;
    events: GriddleDecoratorHandlers;
}

interface ProfilesPageState {
    filter: string;
}

export class UnconnectedProfilesPage extends React.Component<ProfilesPageProps, ProfilesPageState> {

    componentWillMount?(): void {
        this.props.index(this.props.griddleState.pageSize, this.props.griddleState.currentPage);
    }

    componentWillUpdate?(nextProps: ProfilesPageProps, nextState: void | Readonly<{}>) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter
            || nextGriddleState.currentPage !== griddleState.currentPage
            || nextGriddleState.sortId !== griddleState.sortId
            || nextGriddleState.sortAscending !== griddleState.sortAscending
        ) {
            let sortColumnId = "";
            if (nextGriddleState.sortId) {
                sortColumnId = nextGriddleState.sortId.substr("attributes.".length);
                if (!nextGriddleState.sortAscending) {
                    sortColumnId = "-" + sortColumnId;
                }
            }

            this.props.index(
                nextGriddleState.pageSize,
                nextGriddleState.currentPage,
                [sortColumnId],
                [{ name: "display_name", op: "ilike", val: `%${nextGriddleState.filter}%` }]);
        }
    }

    handleDrop = (files: File[]) => {
        console.dir(files);
        this.props.upload(files[0]);
    }

    render(): JSX.Element {
        const {
            griddleState,
            profiles,
        } = this.props;

        ///api/v1/upload/profiles
        return (
            <Container className="ProfilesPage">
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Profiles</Header>
                            <Dropzone
                                onDrop={this.handleDrop}
                                className="dropzone"
                                activeClassName="dropzone-active"
                                rejectClassName="dropzone-reject"
                                style={{}}
                                accept="application/x-apple-aspen-config">
                                <Header as="h3">Drop configuration profile or Click to upload</Header>
                            </Dropzone>

                        {profiles.uploadError &&
                            <Message negative header="Upload error" content={profiles.uploadErrorDetail.message} />
                        }

                        <Griddle
                            data={profiles.items}
                            plugins={[SemanticUIPlugin()]}
                            pageProperties={{
                                currentPage: griddleState.currentPage,
                                pageSize: griddleState.pageSize,
                                recordCount: profiles.recordCount,
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: "ui celled table",
                                    NoResults: "ui message",
                                },
                            }}
                            events={this.props.events}
                            components={{
                                Layout,
                            }}
                        >
                            <RowDefinition>
                                <ColumnDefinition id="id" customComponent={RouteLinkColumn} urlPrefix="/profiles/" />
                                <ColumnDefinition title="Name" id="attributes.display_name" />
                                <ColumnDefinition title="Scope" id="attributes.scope" component={PayloadScopeIcon} />
                                <ColumnDefinition title="UUID" id="attributes.uuid" />
                            </RowDefinition>
                        </Griddle>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}

export const ProfilesPage = connect<ReduxStateProps, ReduxDispatchProps, ProfilesPageProps>(
    (state: RootState, ownProps?: any): ReduxStateProps => ({
        profiles: state.profiles,
    }),
    (dispatch: Dispatch<RootState>, ownProps?: any): ReduxDispatchProps => bindActionCreators({
        index: actions.index,
        upload: actions.upload,
    }, dispatch),
)(griddle(UnconnectedProfilesPage));
