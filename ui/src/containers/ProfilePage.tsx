import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {bindActionCreators} from "redux";
import {RootState} from "../reducers/index";

import Container from "semantic-ui-react/src/elements/Container";
import Header from "semantic-ui-react/src/elements/Header";
import Segment from "semantic-ui-react/src/elements/Segment";
import Grid from "semantic-ui-react/src/collections/Grid";
import { DropdownProps } from "semantic-ui-react/src/modules/Dropdown";

import {SyntheticEvent} from "react";
import {RouteComponentProps} from "react-router";
import {read, ReadActionRequest} from "../store/profiles/actions";
import {patchRelationship, PatchRelationshipActionRequest} from "../store/profiles/actions";
import {
    index as fetchTags, IndexActionRequest,
    post as createTag, PostActionRequest as PostTagActionRequest,
} from "../store/tags/actions";
import {TagDropdown} from "../components/TagDropdown";
import {isArray} from "../guards";
import {JSONAPIDataObject, JSONAPIRelationship} from "../json-api";
import {Tag} from "../store/tags/types";
import {ProfileState} from "../reducers/profile";
import {TagsState} from "../store/tags/reducer";
import {Profile} from "../store/profiles/types";

interface RouteProps {
    id?: string;
}

interface ReduxStateProps {
    profile?: JSONAPIDataObject<Profile>;
    tags: TagsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        profile: state.profile.profile,
        tags: state.tags,
    };
}

interface ReduxDispatchProps {
    read: ReadActionRequest;
    fetchTags: IndexActionRequest;
    createTag: PostTagActionRequest;
    patchRelationship: PatchRelationshipActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>): ReduxDispatchProps {
    return bindActionCreators({
        read,
        fetchTags,
        createTag,
        patchRelationship,
    }, dispatch);
}

interface OwnProps extends RouteComponentProps<RouteProps> {

}

export class UnconnectedProfilePage extends React.Component<OwnProps & ReduxStateProps & ReduxDispatchProps, void | {}> {

    componentWillMount?() {
        const {params: {id}} = this.props.match;
        this.props.read(id, ["tags"]);
        this.props.fetchTags();
    }

    handleAddTag = (event: SyntheticEvent<MouseEvent>, {value}: { value: string }) => {
        const tag: Tag = {
            name: value,
            color: "888888",
        };

        this.props.createTag(tag);
    }

    handleSearchTag = (value: string) => {
        this.props.fetchTags(10, 1, [], [{name: "name", op: "ilike", val: `%${value}%`}]);
    }

    handleChangeTag = (event: React.SyntheticEvent<HTMLElement>, data: DropdownProps): void => {
        const { value } = data;

        const relationships = value.map((v: string) => {
            return {id: v, type: "tags"};
        });

        this.props.patchRelationship(
            "" + this.props.match.params.id, "tags", relationships);
    }

    render() {
        const {
            profile,
            tags,
        } = this.props;

        const tagChoices = tags.items.map((item: JSONAPIDataObject<Tag>) => {
            return {name: item.attributes.name, text: item.attributes.name, value: item.id};
        });

        let profileTags: number[] = [];
        if (profile && profile.relationships && profile.relationships.tags) {
            if (isArray(profile.relationships.tags.data)) {
                profileTags = profile.relationships.tags.data.map((t: JSONAPIRelationship) => parseInt(t.id, 0));
            }

        }

        return (
            <Container className="ProfilePage">
                <TagDropdown
                    loading={false}
                    tags={tagChoices}
                    value={profileTags}
                    onAddItem={this.handleAddTag}
                    onSearch={this.handleSearchTag}
                    onChange={this.handleChangeTag}
                />
                <Segment>
                    <Grid columns={2}>

                        <Grid.Row>
                            <Grid.Column>
                                <Header as="h1">{profile && profile.attributes.display_name}</Header>
                                <p>{profile && profile.attributes.description || "No Description"}</p>
                            </Grid.Column>
                            <Grid.Column>
                                <Header as="h1" color="grey"
                                        textAlign="right">{profile && profile.attributes.uuid}</Header>
                            </Grid.Column>
                        </Grid.Row>

                    </Grid>
                </Segment>

            </Container>
        );
    }
}

export const ProfilePage = connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedProfilePage);
