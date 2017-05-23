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

interface ReduxStateProps {
    profiles: ProfilesState;
}

interface ReduxDispatchProps {
    index: IndexActionRequest;
}

interface ProfilesPageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<any> {
    componentWillMount: () => void;
}

interface ProfilesPageState {
    filter: string;
}

@connect<ReduxStateProps, ReduxDispatchProps, ProfilesPageProps>(
    (state: RootState, ownProps?: any): ReduxStateProps => {
        return { profiles: state.profiles };
    },
    (dispatch: Dispatch<any>): ReduxDispatchProps => {
        return bindActionCreators({
            index: actions.index
        }, dispatch);
    }
)
export class ProfilesPage extends React.Component<ProfilesPageProps, ProfilesPageState> {

    componentWillMount(): void {
        this.props.index();
    }

    handleFilter = (filterText: string) => {
        // TODO: debounce filter text
    };

    render(): JSX.Element {
        const {
            profiles
        } = this.props;

        const eventHandlers = {
            onFilter: this.handleFilter
        };

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
                            pageProperties={profiles.pageProperties}
                            styleConfig={{
                                classNames: {
                                    Table: 'ui celled table'
                                }
                            }}
                            events={eventHandlers}
                        >
                            <RowDefinition>
                                <ColumnDefinition id="id" />
                                <ColumnDefinition title="Scope" id="attributes.scope" component={PayloadScopeIcon} />
                                <ColumnDefinition title="UUID" id="attributes.uuid" />
                                <ColumnDefinition title="Name" id="attributes.display_name" />
                            </RowDefinition>
                        </Griddle>
                    </Grid.Column>
                </Grid>
            </Container>
        );
    }
}