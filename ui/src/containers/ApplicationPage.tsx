import * as React from "react";
import {SyntheticEvent} from "react";
import {connect} from "react-redux";
import {Route, RouteComponentProps} from "react-router";
import {Link} from "react-router-dom";
import {bindActionCreators, Dispatch} from "redux";
import {Breadcrumb, Container, Divider, Grid, Header, Image, Menu} from "semantic-ui-react";
import {DropdownProps} from "semantic-ui-react/src/modules/Dropdown";
import {TagDropdown} from "../components/TagDropdown";
import {isArray} from "../guards";
import {RootState} from "../reducers";
import {
    patchRelationship, PatchRelationshipActionRequest,
    read, ReadActionRequest,
} from "../store/applications/actions";
import {IApplicationState} from "../store/applications/reducer";
import {JSONAPIRelationship, JSONAPIResourceIdentifier} from "../store/json-api";
import {
    index as fetchTags,
    IndexActionRequest,
    post as createTag,
    PostActionRequest as PostTagActionRequest,
} from "../store/tags/actions";
import {ITagsState} from "../store/tags/reducer";
import {Tag} from "../store/tags/types";
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import {ApplicationDeviceStatus} from "./applications/ApplicationDeviceStatus";

interface IRouteProps {
    id: string;
}

export interface IDispatchProps {
    read: ReadActionRequest;
    fetchTags: IndexActionRequest;
    patchRelationship: PatchRelationshipActionRequest;
}

export interface IStateProps {
    application: IApplicationState;
    tags: ITagsState;
}

class UnconnectedApplicationPage extends React.Component<IDispatchProps & IStateProps & RouteComponentProps<IRouteProps>, any> {

    public componentWillMount?() {
        const { match: { params: { id } } } = this.props;

        this.props.read(id, ["tags"]);
        this.props.fetchTags(40);
    }

    public render() {
        const {
            match: { params: { id } },
            application: { data, loading },
            tags,
        } = this.props;

        let appTags: number[] = [];

        if (data && data.data.relationships && data.data.relationships.tags) {
            if (isArray(data.data.relationships.tags.data)) {
                appTags = data.data.relationships.tags.data.map((t: JSONAPIResourceIdentifier) => parseInt(t.id, 0));
            } else {
                appTags = [parseInt(data.data.relationships.tags.data.id, 0)];
            }
        }

        return (
            <Container>
                <Divider hidden />
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section><Link to={`/applications`}>Applications</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section>{data ? data.data.attributes.display_name : "App"}</Breadcrumb.Section>
                </Breadcrumb>
                <Divider hidden />

                <Grid columns={2}>
                    <Grid.Column width={4}>
                        <Image size="medium" rounded src={data ? data.data.attributes.artwork_url512 : null}/>
                    </Grid.Column>
                    <Grid.Column width={12}>
                        <Header as="h1">
                            {data ? data.data.attributes.display_name + " " + data.data.attributes.version : "Loading..."}
                            <Header.Subheader>
                                {data ? data.data.attributes.artist_name : "Loading..."}
                            </Header.Subheader>
                        </Header>

                        <Header as="h4">Release notes</Header>
                        <p>{data ? data.data.attributes.release_notes : ""}</p>

                        <Header as="h4">Minimum OS</Header>
                        <p>{data ? data.data.attributes.minimum_os_version : ""}</p>
                    </Grid.Column>
                </Grid>

                <TagDropdown
                    loading={tags.loading}
                    tags={tags.items}
                    value={appTags}
                    onAddItem={this.handleAddTag}
                    onSearch={this.handleSearchTag}
                    onChange={this.handleChangeTag}
                />


                <Menu pointing secondary color="purple" inverted>
                    <MenuItemLink to={`/applications/id/${id}/devices`}>Device Status</MenuItemLink>
                </Menu>

                <Route path="/applications/id/:id/devices" component={ApplicationDeviceStatus}/>
            </Container>
        );
    }

    protected handleAddTag = (event: SyntheticEvent<MouseEvent>, { value }: { value: string }) => {
        const tag: Tag = {
            color:  "888888",
            name: value,
        };

        this.props.postRelated<Tag>("" + this.props.application.data.data.id, "tags", tag);
    };

    protected handleSearchTag = (value: string) => {
        this.props.fetchTags(10, 1, [], [{name: "name", op: "ilike", val: `%${value}%`}]);
    };

    protected handleChangeTag = (event: React.SyntheticEvent<HTMLElement>, data: DropdownProps): void => {
        const value = (data.value as string[]);

        const relationships = value.map((v: string) => {
            return {id: v, type: "tags"};
        });

        this.props.patchRelationship(
            "" + this.props.match.params.id, "tags", relationships);
    };
}

export const ApplicationPage = connect<IStateProps, IDispatchProps>(
    (state: RootState) => ({
        application: state.application,
        tags: state.tags,
    }),
    (dispatch: Dispatch) => bindActionCreators({
        fetchTags,
        patchRelationship,
        read,
    }, dispatch),
)(UnconnectedApplicationPage);
