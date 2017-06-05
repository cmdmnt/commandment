import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RootState} from "../reducers/index";
import {bindActionCreators} from "redux";
import {Container, Segment, Grid, Header} from 'semantic-ui-react';
import {read, ReadActionRequest} from "../actions/profiles";
import {RouteComponentProps} from "react-router";
import {TagDropdown} from "../components/TagDropdown";
import {JSONAPIObject, JSONAPIRelationship} from "../json-api";
import {Profile, Tag} from "../models";
import {
    index as fetchTags, IndexActionRequest,
    post as createTag, PostActionRequest as PostTagActionRequest
} from '../actions/tags';
import {patchRelationship, PatchRelationshipActionRequest} from "../actions/profiles";
import {SyntheticEvent} from "react";
import {ProfileState} from "../reducers/profile";
import {TagsState} from "../reducers/tags";

interface RouteProps {
    id?: string;
}

interface ReduxStateProps {
    profile?: JSONAPIObject<Profile>;
    tags: TagsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        profile: state.profile.profile,
        tags: state.tags
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
        patchRelationship
    }, dispatch);
}

interface OwnProps extends RouteComponentProps<RouteProps> {

}

@connect<ReduxStateProps, ReduxDispatchProps, OwnProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class ProfilePage extends React.Component<OwnProps & ReduxStateProps & ReduxDispatchProps, void | {}> {

    componentWillMount?() {
        const { params: { id } } = this.props.match;
        this.props.read(id, ['tags']);
        this.props.fetchTags();
    }

    handleAddTag = (event: SyntheticEvent<MouseEvent>, { value }: { value: string }) => {
        const tag: Tag = {
            name: value,
            color: '888888'
        };

        this.props.createTag(tag);
    };

    handleSearchTag = (value: string) => {
        this.props.fetchTags(10, 1, [], [{'name': 'name', 'op': 'ilike', 'val': `%${value}%`}]);
    };

    handleApplyTags = (event: SyntheticEvent<any>, { value: values }) => {
        const relationships = values.map((v: number) => {
            return {"id": ''+v, "type": "tags"};
        });

        this.props.patchRelationship(
            ''+this.props.match.params.id, 'tags', relationships);
    };


    render() {
        const {
            profile,
            tags
        } = this.props;

        const tagChoices = tags.items.map((item: JSONAPIObject<Tag>) => {
            return {name: item.attributes.name, text: item.attributes.name, value: item.id};
        });

        let profileTags: Array<number> = [];
        if (profile && profile.relationships) {
            profileTags = profile.relationships.tags &&
                profile.relationships.tags.data.map((t: JSONAPIRelationship) => parseInt(t.id, 0));
        }

        return (
            <Container className='ProfilePage'>
                <TagDropdown
                    loading={false}
                    tags={tagChoices}
                    value={profileTags}
                    onAddItem={this.handleAddTag}
                    onSearch={this.handleSearchTag}
                    onChange={this.handleApplyTags}
                />
                <Segment>
                <Grid columns={2}>

                    <Grid.Row>
                        <Grid.Column>
                            <Header as="h1">{profile && profile.attributes.display_name}</Header>
                            <p>{profile && profile.attributes.description || 'No Description'}</p>
                        </Grid.Column>
                        <Grid.Column>
                            <Header as="h1" color="grey" textAlign='right'>{profile && profile.attributes.uuid}</Header>
                        </Grid.Column>
                    </Grid.Row>




                </Grid>
                </Segment>

            </Container>
        )
    }
}