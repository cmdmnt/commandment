import * as React from "react";
import {connect, Dispatch} from "react-redux";

import {Route, RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import Grid from "semantic-ui-react/src/collections/Grid";
import Menu from "semantic-ui-react/src/collections/Menu";
import Container from "semantic-ui-react/src/elements/Container";
import Segment from "semantic-ui-react/src/elements/Segment";
import Dropdown, { DropdownProps } from "semantic-ui-react/src/modules/Dropdown";
import { DropdownItemProps } from "semantic-ui-react/src/modules/Dropdown/DropdownItem";
import {
    CacheFetchActionRequest, fetchDeviceIfRequired,
    inventory, InventoryActionRequest,
    patchRelationship, PatchRelationshipActionRequest,
    postRelated, PostRelatedActionRequest,
    push, PushActionRequest,
    test, TestActionRequest,
} from "../store/device/actions";
import {MacOSDeviceDetail} from "../components/MacOSDeviceDetail";
import {DeviceState} from "../store/device/device";
import {RootState} from "../reducers/index";

import {SyntheticEvent} from "react";
import {
index as fetchTags, IndexActionRequest,
post as createTag, PostActionRequest as PostTagActionRequest,
} from "../actions/tags";
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import {TagDropdown} from "../components/TagDropdown";
import {isArray} from "../guards";
import {JSONAPIDataObject, JSONAPIRelationship} from "../json-api";
import {Tag} from "../models";
import {TagsState} from "../reducers/tags";
import {getPercentCapacityUsed} from "../selectors/device";
import {DeviceApplications} from "./devices/DeviceApplications";
import {DeviceCertificates} from "./devices/DeviceCertificates";
import {DeviceCommands} from "./devices/DeviceCommands";
import {DeviceDetail} from "./devices/DeviceDetail";
import {DeviceOSUpdates} from "./devices/DeviceOSUpdates";
import {DeviceProfiles} from "./devices/DeviceProfiles";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";

interface OwnProps {

}

interface ReduxStateProps {
    device: DeviceState;
    tags: TagsState;
    percentCapacityUsed: number;
}

function mapStateToProps(state: RootState, ownProps?: OwnProps): ReduxStateProps {
    return {
        device: state.device,
        percentCapacityUsed: getPercentCapacityUsed(state),
        tags: state.tags,
    };
}

interface ReduxDispatchProps {
    push: PushActionRequest;
    inventory: InventoryActionRequest;
    test: TestActionRequest;
    fetchTags: IndexActionRequest;
    fetchDeviceIfRequired: CacheFetchActionRequest;
    createTag: PostTagActionRequest;
    patchRelationship: PatchRelationshipActionRequest;
    postRelated: PostRelatedActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: OwnProps): ReduxDispatchProps {
    return bindActionCreators({
        createTag,
        fetchDeviceIfRequired,
        fetchTags,
        inventory,
        patchRelationship,
        postRelated,
        push,
        test,
    }, dispatch);
}

interface RouteParameters {
    id: number;
}

interface DevicePageProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<RouteParameters> {
    componentDidMount: () => void;
}

interface DevicePageState {
    filter: string;
}

class BaseDevicePage extends React.Component<DevicePageProps, DevicePageState> {

    protected handleAction = (e: SyntheticEvent<any>, {value}: {value: string}) => {
        e.preventDefault();
        switch (value) {
            case "push":
                this.props.push("" + this.props.device.device.id);
                break;
            case "inventory":
                this.props.inventory("" + this.props.device.device.id);
                break;
            case "test":
                this.props.test("" + this.props.device.device.id);
                break;
        }
    };

    protected handleAddTag = (event: SyntheticEvent<MouseEvent>, { value }: { value: string }) => {
        const tag: Tag = {
            color: "888888",
            name: value,
        };

        this.props.postRelated<Tag>("" + this.props.device.device.id, "tags", tag);
    };

    protected handleSearchTag = (value: string) => {
        this.props.fetchTags(10, 1, [], [{name: "name", op: "ilike", val: `%${value}%`}]);
    };

    protected handleChangeTag = (event: React.SyntheticEvent<HTMLElement>, data: DropdownProps): void => {
        const { value } = data;

        const relationships = value.map((v: string) => {
            return {id: v, type: "tags"};
        });

        this.props.patchRelationship(
            "" + this.props.match.params.id, "tags", relationships);
    };

    public componentDidMount(): void {
        this.props.fetchDeviceIfRequired("" + this.props.match.params.id, ["tags"]);
        this.props.fetchTags(40);
    }

    public render(): JSX.Element {
        const {
            device,
            match: {params: {id: device_id}},
            tags,
        } = this.props;

        const tagChoices: DropdownItemProps[] = tags.items.map((item: JSONAPIDataObject<Tag>) => {
            return {name: item.attributes.name, text: item.attributes.name, value: item.id};
        });

        let deviceTags: number[] = [];
        if (device.device && device.device.relationships && device.device.relationships.tags) {
            if (isArray(device.device.relationships.tags.data)) {
                deviceTags = device.device.relationships.tags.data.map((t: JSONAPIRelationship) => parseInt(t.id, 0));
            } else {
                deviceTags = [parseInt(device.device.relationships.tags.data.id, 0)];
            }
        }

        return (
            <Container className="DevicePage">
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Segment>
                                {device && <MacOSDeviceDetail device={device}/>}
                            </Segment>
                            <Segment attached>
                                <Dropdown inline button text="action" onChange={this.handleAction} options={[
                                    {text: "Force Push", value: "push"},
                                    {text: "Inventory", value: "inventory"},
                                    {text: "Test", value: "test"},
                                ]}></Dropdown>
                                <TagDropdown
                                    loading={device.tagsLoading}
                                    tags={tagChoices}
                                    value={deviceTags}
                                    onAddItem={this.handleAddTag}
                                    onSearch={this.handleSearchTag}
                                    onChange={this.handleChangeTag}
                                />
                            </Segment>
                            <Menu pointing secondary color="purple" inverted>
                                <MenuItemLink to={`/devices/${device_id}/detail`}>Detail</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/certificates`}>Certificates</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/commands`}>Commands</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/installed_applications`}>Applications</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/installed_profiles`}>Profiles</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/available_os_updates`}>Updates</MenuItemLink>
                            </Menu>
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column>
                            <Route path="/devices/:id/detail" component={DeviceDetail}/>
                            <Route path="/devices/:id/certificates" component={DeviceCertificates}/>
                            <Route path="/devices/:id/commands" component={DeviceCommands}/>
                            <Route path="/devices/:id/installed_applications" component={DeviceApplications}/>
                            <Route path="/devices/:id/installed_profiles" component={DeviceProfiles}/>
                            <Route path="/devices/:id/available_os_updates" component={DeviceOSUpdates}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }
}

export const DevicePage = connect<ReduxStateProps, ReduxDispatchProps, DevicePageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(BaseDevicePage);
