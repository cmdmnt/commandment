import * as React from "react";
import {SyntheticEvent} from "react";
import {connect} from "react-redux";

import {RouteComponentProps} from "react-router";
import {Link} from "react-router-dom";
import {bindActionCreators, Dispatch} from "redux";
import {MacOSDeviceDetail} from "../components/devices/MacOSDeviceDetail";
import {isArray} from "../guards";
import {RootState} from "../reducers/index";
import {getPercentCapacityUsed} from "../selectors/device";
import {
    CacheFetchActionRequest,
    clearPasscode,
    ClearPasscodeActionRequest,
    fetchDeviceIfRequired,
    inventory,
    InventoryActionRequest,
    lock,
    LockActionRequest,
    patchRelationship,
    PatchRelationshipActionRequest,
    postRelated,
    PostRelatedActionRequest,
    push,
    PushActionRequest,
    restart,
    RestartActionRequest,
    shutdown,
    ShutdownActionRequest,
} from "../store/device/actions";
import {DeviceState} from "../store/device/reducer";
import {JSONAPIRelationship, JSONAPIResourceIdentifier} from "../store/json-api";
import {
    index as fetchTags,
    IndexActionRequest,
    post as createTag,
    PostActionRequest as PostTagActionRequest,
} from "../store/tags/actions";
import {ITagsState} from "../store/tags/reducer";
import {Tag} from "../store/tags/types";

import {Breadcrumb, Container, Divider, DropdownProps} from "semantic-ui-react";

import {DEPDeviceDetail} from "../components/devices/DEPDeviceDetail";
import {IOSDeviceDetail} from "../components/devices/IOSDeviceDetail";
import {DeviceOperatingSystem, operatingSystem} from "../store/device/types";

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
}

function mapDispatchToProps(dispatch: Dispatch, ownProps?: any): IReduxDispatchProps {
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
    }, dispatch);
}

interface IRouteParameters {
    id?: string;
}

type DevicePageProps = IReduxStateProps & IReduxDispatchProps & RouteComponentProps<IRouteParameters>;

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

        let deviceTags: number[] = [];
        if (device.device && device.device.relationships && device.device.relationships.tags) {
            if (isArray(device.device.relationships.tags.data)) {
                deviceTags = device.device.relationships.tags.data.map((t: JSONAPIResourceIdentifier) => parseInt(t.id, 0));
            } else {
                deviceTags = [parseInt(device.device.relationships.tags.data.id, 0)];
            }
        }

        let DetailComponent = <span>Loading</span>;
        let showTools = true;

        const actions = {
            clearPasscode,
            inventory,
            lock,
            push,
            restart,
            shutdown,
        };

        if (device.device && !device.loading) {
            if (device.device.attributes.is_dep && device.device.attributes.is_enrolled === false) {
                DetailComponent = <DEPDeviceDetail device={device}/>;
                showTools = false;
            } else if (operatingSystem(device.device.attributes.model_name) === DeviceOperatingSystem.iOS) {
                DetailComponent = <IOSDeviceDetail device={device}
                                                   tags={tags}
                                                   deviceTags={deviceTags}
                                                   onAddTag={this.handleAddTag}
                                                   onChangeTag={this.handleChangeTag}
                                                   onSearchTag={this.handleSearchTag}
                                                   {...actions} />;
            } else {
                DetailComponent = <MacOSDeviceDetail device={device}
                                                     tags={tags}
                                                     deviceTags={deviceTags}
                                                     onAddTag={this.handleAddTag}
                                                     onChangeTag={this.handleChangeTag}
                                                     onSearchTag={this.handleSearchTag}
                                                     {...actions} />;
            }
        }

        return (
            <Container className="DevicePage">
                <Divider hidden />
                <Breadcrumb>
                    <Breadcrumb.Section><Link to={`/`}>Home</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section><Link to={`/devices`}>Devices</Link></Breadcrumb.Section>
                    <Breadcrumb.Divider />
                    <Breadcrumb.Section>{device.device ? device.device.attributes.device_name : "Device"}</Breadcrumb.Section>
                </Breadcrumb>

                {DetailComponent}

            </Container>
        );
    }

    protected handleAddTag = (event: SyntheticEvent<MouseEvent>, { value }: { value: string }) => {
        const tag: Tag = {
            color:  "888888",
            name: value,
        };

        this.props.postRelated<Tag>("" + this.props.device.device.id, "tags", tag);
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

export const DevicePage = connect<IReduxStateProps, IReduxDispatchProps, DevicePageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(BaseDevicePage);
