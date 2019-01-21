import * as React from "react";
import {connect} from "react-redux";
import {Dispatch} from "redux";

import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {RootState} from "../reducers/index";
import * as actions from "../store/profiles/actions";
import {IndexActionRequest, UploadActionRequest} from "../store/profiles/actions";
import {ProfilesState} from "../store/profiles/reducer";
import {ProfilesTable} from "../components/react-tables/ProfilesTable";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import {Link} from "react-router-dom";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import {ToggleSelectionActionCreator} from "../store/table/actions";
import * as tableActions from "../store/table/actions";
import {ITableState} from "../store/table/reducer";
import {IReactTableState} from "../store/table/types";
import {FlaskFilterOperation} from "../flask-rest-jsonapi";
import {FlaskFilter} from "../flask-rest-jsonapi";

interface IReduxStateProps {
    profiles: ProfilesState;
    table: ITableState;
}

interface IReduxDispatchProps {
    index: IndexActionRequest;
    upload: UploadActionRequest;
    toggleSelection: ToggleSelectionActionCreator;
}

interface IProfilesPageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<any> {
    componentWillMount: () => void;
}

interface IProfilesPageState {
    filter: string;
}

export class UnconnectedProfilesPage extends React.Component<IProfilesPageProps, IProfilesPageState> {

    public componentWillMount?() {
        this.props.index();
    }

    public render(): JSX.Element {
        const {
            profiles,
            toggleSelection,
            table,
        } = this.props;

        return (
            <Container className="ProfilesPage">
                <Divider hidden />
                <Header as="h1">Profiles</Header>
                <Dropdown text="Add" icon="plus" labeled button className="icon">
                    <Dropdown.Menu>
                        <Dropdown.Item as={Link} to="/profiles/add/custom">Custom Profile (.mobileconfig)</Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>
                <Divider hidden />
                <ProfilesTable
                    data={profiles.items}
                    loading={profiles.loading}
                    toggleSelection={toggleSelection}
                    isSelected={(key: string) => table.selection.indexOf(key) !== -1}
                    onFetchData={this.fetchData}
                />
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

export const ProfilesPage = connect<IReduxStateProps, IReduxDispatchProps, IProfilesPageProps>(
    (state: RootState, ownProps?: any): IReduxStateProps => ({
        profiles: state.profiles,
        table: state.table,
    }),
    (dispatch: Dispatch, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        index: actions.index,
        toggleSelection: tableActions.toggleSelection,
        upload: actions.upload,
    }, dispatch),
)(UnconnectedProfilesPage);
