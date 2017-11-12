import * as React from 'react';
import {connect, Dispatch} from 'react-redux';

import {bindActionCreators} from "redux";
import {IRootState} from "../reducers/index";
import {Route, RouteComponentProps} from "react-router";
import {
    inventory, InventoryActionRequest,
    push, PushActionRequest,
    test, TestActionRequest,
    fetchDeviceIfRequired, CacheFetchActionRequest,
    postRelated, PostRelatedActionRequest,
    patchRelationship, PatchRelationshipActionRequest
} from "../actions/devices";
import {MacOSDeviceDetail} from '../components/MacOSDeviceDetail';
import {DeviceState} from "../reducers/device";
import {Container, Grid, Menu, Segment, Dropdown, DropdownItemProps, DropdownProps} from 'semantic-ui-react';
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import {SyntheticEvent} from "react";
import {DeviceCertificates} from "./devices/DeviceCertificates";
import {DeviceCommands} from "./devices/DeviceCommands";
import {DeviceApplications} from "./devices/DeviceApplications";
import {DeviceProfiles} from "./devices/DeviceProfiles";
import {DeviceOSUpdates} from "./devices/DeviceOSUpdates";
import {DeviceDetail} from "./devices/DeviceDetail";
import {TagDropdown} from "../components/TagDropdown";
import {TagsState} from "../reducers/tags";
import {
index as fetchTags, IndexActionRequest,
post as createTag, PostActionRequest as PostTagActionRequest
} from '../actions/tags';
import {Tag} from "../models";
import {JSONAPIObject, JSONAPIRelationship} from "../json-api";
import {getPercentCapacityUsed} from "../selectors/device";
import {isArray} from "../guards";

interface OwnProps {

}

interface ReduxStateProps {
    device: DeviceState;
    tags: TagsState;
    percentCapacityUsed: number;
}

function mapStateToProps(state: IRootState, ownProps?: OwnProps): ReduxStateProps {
    return {
        device: state.device,
        tags: state.tags,
        percentCapacityUsed: getPercentCapacityUsed(state)
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

function mapDispatchToProps(dispatch: Dispatch<IRootState>, ownProps?: OwnProps): ReduxDispatchProps {
    return bindActionCreators({
        push,
        inventory,
        test,
        fetchTags,
        fetchDeviceIfRequired,
        createTag,
        patchRelationship,
        postRelated
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

    handleAction = (e: SyntheticEvent<any>, {value}: {value: string}) => {
        e.preventDefault();
        switch (value) {
            case 'push':
                this.props.push(''+this.props.device.device.id);
                break;
            case 'inventory':
                this.props.inventory(''+this.props.device.device.id);
                break;
            case 'test':
                this.props.test(''+this.props.device.device.id);
                break;
        }
    };

    handleAddTag = (event: SyntheticEvent<MouseEvent>, { value }: { value: string }) => {
        const tag: Tag = {
            name: value,
            color: '888888'
        };

        this.props.postRelated<Tag>(''+this.props.device.device.id, "tags", tag);
    };

    handleSearchTag = (value: string) => {
        this.props.fetchTags(10, 1, [], [{'name': 'name', 'op': 'ilike', 'val': `%${value}%`}]);
    };

    handleChangeTag = (event: React.SyntheticEvent<HTMLElement>, data: DropdownProps): void => {
        const { value } = data;

        const relationships = value.map((v: string) => {
            return {"id": v, "type": "tags"};
        });

        this.props.patchRelationship(
            ''+this.props.match.params.id, 'tags', relationships);
    };

    componentDidMount(): void {
        this.props.fetchDeviceIfRequired(''+this.props.match.params.id, ['tags']);
        this.props.fetchTags(40);
    }

    render(): JSX.Element {
        const {
            device,
            match: {params: {id: device_id}},
            tags
        } = this.props;

        const tagChoices: Array<DropdownItemProps> = tags.items.map((item: JSONAPIObject<Tag>) => {
            return {name: item.attributes.name, text: item.attributes.name, value: item.id};
        });

        let deviceTags: Array<number> = [];
        if (device.device && device.device.relationships && device.device.relationships.tags) {
            if (isArray(device.device.relationships.tags.data)) {
                deviceTags = device.device.relationships.tags.data.map((t: JSONAPIRelationship) => parseInt(t.id, 0));
            } else {
                deviceTags = [parseInt(device.device.relationships.tags.data.id, 0)];
            }
        }

        return (
            <Container className='DevicePage'>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Dropdown inline text="action" onChange={this.handleAction} options={[
                                {text: 'Force Push', value: 'push'},
                                {text: 'Inventory', value: 'inventory'},
                                {text: 'Test', value: 'test'}
                            ]}></Dropdown>
                            <TagDropdown
                                loading={device.tagsLoading}
                                tags={tagChoices}
                                value={deviceTags}
                                onAddItem={this.handleAddTag}
                                onSearch={this.handleSearchTag}
                                onChange={this.handleChangeTag}
                            />
                            <Segment>
                                {device && <MacOSDeviceDetail device={device}/>}
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
                            <Route path='/devices/:id/detail' component={DeviceDetail}/>
                            <Route path='/devices/:id/certificates' component={DeviceCertificates}/>
                            <Route path='/devices/:id/commands' component={DeviceCommands}/>
                            <Route path='/devices/:id/installed_applications' component={DeviceApplications}/>
                            <Route path='/devices/:id/installed_profiles' component={DeviceProfiles}/>
                            <Route path='/devices/:id/available_os_updates' component={DeviceOSUpdates}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }
}

export const DevicePage = connect<ReduxStateProps, ReduxDispatchProps, DevicePageProps>(
    mapStateToProps,
    mapDispatchToProps
)(BaseDevicePage);