import * as React from "react";
import {connect, Dispatch} from "react-redux";

import Grid from "semantic-ui-react/src/collections/Grid";
import Message from "semantic-ui-react/src/collections/Message";
import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";

import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {griddle, GriddleDecoratorHandlers, GriddleDecoratorState} from "../hoc/griddle";
import {RootState} from "../reducers/index";
import * as actions from "../store/profiles/actions";
import {IndexActionRequest, UploadActionRequest} from "../store/profiles/actions";
import {ProfilesState} from "../store/profiles/reducer";
import {ProfilesTable} from "../components/react-tables/ProfilesTable";
import Dropdown from "semantic-ui-react/dist/commonjs/modules/Dropdown/Dropdown";
import {Link} from "react-router-dom";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

interface IReduxStateProps {
    profiles: ProfilesState;
}

interface IReduxDispatchProps {
    index: IndexActionRequest;
    upload: UploadActionRequest;
}

interface IProfilesPageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<any> {
    componentWillMount: () => void;
    griddleState: GriddleDecoratorState;
    events: GriddleDecoratorHandlers;
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
            griddleState,
            profiles,
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
                />
            </Container>
        );
    }
}

export const ProfilesPage = connect<IReduxStateProps, IReduxDispatchProps, IProfilesPageProps>(
    (state: RootState, ownProps?: any): IReduxStateProps => ({
        profiles: state.profiles,
    }),
    (dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps => bindActionCreators({
        index: actions.index,
        upload: actions.upload,
    }, dispatch),
)(griddle(UnconnectedProfilesPage));
