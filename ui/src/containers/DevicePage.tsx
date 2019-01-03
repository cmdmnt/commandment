import * as React from "react";
import {connect, Dispatch} from "react-redux";

import {Route, RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {MacOSDeviceDetail} from "../components/devices/MacOSDeviceDetail";
import {RootState} from "../reducers/index";
import {
    CacheFetchActionRequest, clearPasscode,
    ClearPasscodeActionRequest, fetchDeviceIfRequired,
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
import {Link} from "react-router-dom";
import {isArray} from "../guards";
import {JSONAPIDataObject, JSONAPIRelationship} from "../json-api";
import {getPercentCapacityUsed} from "../selectors/device";
import {
index as fetchTags, IndexActionRequest,
post as createTag, PostActionRequest as PostTagActionRequest,
} from "../store/tags/actions";
import {ITagsState} from "../store/tags/reducer";
import {Tag} from "../store/tags/types";

import Breadcrumb from "semantic-ui-react/dist/commonjs/collections/Breadcrumb/Breadcrumb";

import Container from "semantic-ui-react/dist/commonjs/elements/Container/Container";
import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";

import Dropdown, { DropdownProps } from "semantic-ui-react/src/modules/Dropdown";
import { DropdownItemProps } from "semantic-ui-react/src/modules/Dropdown/DropdownItem";
import {DEPDeviceDetail} from "../components/devices/DEPDeviceDetail";

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

        let DetailComponent = <span>Loading</span>;
        let showTools = true;

        if (device.device && !device.loading) {
            if (device.device.attributes.is_dep) {
                DetailComponent = <DEPDeviceDetail device={device} />;
                showTools = false;
            } else {
                DetailComponent = <MacOSDeviceDetail device={device} tagChoices={tagChoices} deviceTags={deviceTags} />;
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
        const { value } = data;

        const relationships = value.map((v: string) => {
            return {id:  v, type: "tags"};
        });

        this.props.patchRelationship(
            "" + this.props.match.params.id, "tags", relationships);
    };
}

export const DevicePage = connect<IReduxStateProps,  IReduxDispatchProps, IDevicePageProps>(
    mapStateToProps,
    mapDispatchToProps,
)(BaseDevicePage);
