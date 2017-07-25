import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {Grid, Container, Table, Header} from 'semantic-ui-react';
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';

import {bindActionCreators} from "redux";
import * as actions from '../actions/profiles';
import {RootState} from "../reducers/index";
import {RouteComponentProps} from "react-router";
import {ProfilesState} from "../reducers/profiles";
import {IndexActionRequest} from "../actions/profiles";
import {PayloadScopeIcon} from '../components/griddle/PayloadScopeIcon';
import {SimpleLayout as Layout} from "../components/griddle/SimpleLayout";
import {SemanticUIPlugin} from "../griddle-plugins/semantic-ui/index";
import {griddle, GriddleDecoratorHandlers, GriddleDecoratorState} from "../hoc/griddle";
import {RouteLinkColumn} from "../components/griddle/RouteLinkColumn";

interface ReduxStateProps {
    profiles: ProfilesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        profiles: state.profiles
    }
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: any): ReduxDispatchProps {
    return bindActionCreators({
        index: actions.index
    }, dispatch);
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
            let sortColumnId = '';
            if (nextGriddleState.sortId) {
                sortColumnId = nextGriddleState.sortId.substr('attributes.'.length);
                if (!nextGriddleState.sortAscending) {
                    sortColumnId = '-' + sortColumnId;
                }
            }

            this.props.index(
                nextGriddleState.pageSize,
                nextGriddleState.currentPage,
                [sortColumnId],
                [{ name: 'display_name', op: 'ilike', val: `%${nextGriddleState.filter}%` }]);
        }
    }

    render(): JSX.Element {
        const {
            griddleState,
            profiles
        } = this.props;

        return (
            <Container className='ProfilesPage'>
                <Grid>
                    <Grid.Column>
                        <Header as="h1">Profiles</Header>

                        <form method='POST' action='/api/v1/upload/profiles' encType='multipart/form-data'>
                            <input type='file' name='file' accept='application/x-apple-aspen-config' />
                            <input type='submit' />
                        </form>

                        <Griddle
                            data={profiles.items}
                            plugins={[SemanticUIPlugin()]}
                            pageProperties={{
                                currentPage: griddleState.currentPage,
                                pageSize: griddleState.pageSize,
                                recordCount: profiles.recordCount
                            }}
                            styleConfig={{
                                classNames: {
                                    Table: 'ui celled table',
                                    NoResults: 'ui message'
                                }
                            }}
                            events={this.props.events}
                            components={{
                                Layout
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
    mapStateToProps,
    mapDispatchToProps
)(griddle(UnconnectedProfilesPage));
