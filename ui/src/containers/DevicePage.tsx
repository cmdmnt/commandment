import * as React from "react";
import {connect, Dispatch} from "react-redux";

import {Route, RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {MacOSDeviceDetail} from "../components/MacOSDeviceDetail";
import {RootState} from "../reducers/index";
import {
    clearPasscode, ClearPasscodeActionRequest,
    fetchDeviceIfRequired, CacheFetchActionRequest,
    inventory, InventoryActionRequest,
    lock, LockActionRequest,
    patchRelationship, PatchRelationshipActionRequest,
    postRelated, PostRelatedActionRequest,
    push, PushActionRequest,
    restart, RestartActionRequest,
    shutdown, ShutdownActionRequest,
    test, TestActionRequest,
} from "../store/device/actions";
import {DeviceState} from "../store/device/device";

import {SyntheticEvent} from "react";
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import {TagDropdown} from "../components/TagDropdown";
import {isArray} from "../guards";
import {JSONAPIDataObject, JSONAPIRelationship} from "../json-api";
import {getPercentCapacityUsed} from "../selectors/device";
import {
index as fetchTags, IndexActionRequest,
post as createTag, PostActionRequest as PostTagActionRequest,
} from "../store/tags/actions";
import {ITagsState} from "../store/tags/reducer";
import {Tag} from "../store/tags/types";
import {DeviceApplications} from "./devices/DeviceApplications";
import {DeviceCertificates} from "./devices/DeviceCertificates";
import {DeviceCommands} from "./devices/DeviceCommands";
import {DeviceDetail} from "./devices/DeviceDetail";
import {DeviceOSUpdates} from "./devices/DeviceOSUpdates";
import {DeviceProfiles} from "./devices/DeviceProfiles";

import Grid from "semantic-ui-react/src/collections/Grid";
import Menu from "semantic-ui-react/src/collections/Menu";
import Container from "semantic-ui-react/src/elements/Container";
import Segment from "semantic-ui-react/src/elements/Segment";
import Button from "semantic-ui-react/dist/commonjs/elements/Button/Button";
import Dropdown, { DropdownProps } from "semantic-ui-react/src/modules/Dropdown";
import { DropdownItemProps } from "semantic-ui-react/src/modules/Dropdown/DropdownItem";
import Header from "semantic-ui-react/dist/commonjs/elements/Header/Header";
import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";
import {ButtonLink} from "../components/semantic-ui/ButtonLink";
import {DeviceRename} from "./DeviceRename";

interface IReduxStateProps {
    device: DeviceState;
    tags: ITagsState;
    percentCapacityUsed: number;
}

function mapStateToProps(state: RootState, ownProps?: any): IReduxStateProps {
    return {
        device: state.device,
        percentCapacityUsed: getPercentCapacityUsed(state),
        tags: state.tags,
    };
}

interface IReduxDispatchProps {
    clearPasscode: ClearPasscodeActionRequest;
    createTag: PostTagActionRequest;
    fetchDeviceIfRequired: CacheFetchActionRequest;
    fetchTags: IndexActionRequest;
    inventory: InventoryActionRequest;
    lock: LockActionRequest;
    patchRelationship: PatchRelationshipActionRequest;
    postRelated: PostRelatedActionRequest;
    push: PushActionRequest;
    restart: RestartActionRequest;
    shutdown: ShutdownActionRequest;
    test: TestActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<RootState>, ownProps?: any): IReduxDispatchProps {
    return bindActionCreators({
        clearPasscode,
        createTag,
        fetchDeviceIfRequired,
        fetchTags,
        inventory,
        lock,
        patchRelationship,
        postRelated,
        push,
        restart,
        shutdown,
        test,
    }, dispatch);
}

interface IRouteParameters {
    id: number;
}

interface DevicePageProps extends IReduxStateProps, IReduxDispatchProps, RouteComponentProps<IRouteParameters> {
    componentDidMount: () => void;
}

interface IDevicePageState {
    filter: string;
}

class BaseDevicePage extends React.Component<DevicePageProps, IDevicePageState> {

    public componentDidMount(): void {
        this.props.fetchDeviceIfRequired("" + this.props.match.params.id, ["tags"]);
        this.props.fetchTags(40);
    }

    public render(): JSX.Element {
        const {
            device,
            match: {params: {id: device_id}},
            tags,

            clearPasscode,
            inventory,
            lock,
            push,
            restart,
            shutdown,
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
                            <Segment attached>
                                {device && <MacOSDeviceDetail device={device}/>}
                            </Segment>
                            <Segment attached>
                                <Button icon labelPosition="left" onClick={() => restart(device.device.id)}>
                                    <Icon name="refresh" />
                                    Restart
                                </Button>
                                <Button icon labelPosition="left" onClick={() => shutdown(device.device.id)}>
                                    <Icon name="arrow down" />
                                    Shut down
                                </Button>
                                <Button icon labelPosition="left" onClick={() => clearPasscode(device.device.id)}>
                                    <Icon name="delete" />
                                    Clear Passcode
                                </Button>
                                <Button icon labelPosition="left" onClick={() => lock(device.device.id)}>
                                    <Icon name="lock" />
                                    Lock
                                </Button>
                                <Button icon labelPosition="left" onClick={() => inventory(device.device.id)}>
                                    <Icon name="search" />
                                    Full Inventory
                                </Button>
                                <Button icon labelPosition="left" onClick={() => push(device.device.id)}>
                                    <Icon name="pushed" />
                                    Blank Push
                                </Button>
                                <ButtonLink to={`/devices/${device_id}/rename`}>
                                    Rename
                                </ButtonLink>
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

                            <Route path="/devices/:id/rename" component={DeviceRename}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }

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
}

export const DevicePage = connect<IReduxStateProps, IReduxDispatchProps, DevicePageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(BaseDevicePage);
