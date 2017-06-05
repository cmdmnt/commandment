import * as React from 'react';
import {connect, Dispatch} from 'react-redux';

import {bindActionCreators} from "redux";
import {RootState} from "../reducers/index";
import {Route, RouteComponentProps} from "react-router";
import {
    inventory, InventoryActionRequest,
    push, PushActionRequest,
    test, TestActionRequest,
    fetchDeviceIfRequired, CacheFetchActionRequest,
    patchRelationship, PatchRelationshipActionRequest
} from "../actions/devices";
import {MacOSDeviceDetail} from '../components/MacOSDeviceDetail';
import {DeviceState} from "../reducers/device";
import {Container, Grid, Menu, Segment, Dropdown} from 'semantic-ui-react';
import {MenuItemLink} from "../components/semantic-ui/MenuItemLink";
import {SyntheticEvent} from "react";
import {DeviceCertificates} from "./devices/DeviceCertificates";
import {DeviceCommands} from "./devices/DeviceCommands";
import {DeviceApplications} from "./devices/DeviceApplications";
import {DeviceProfiles} from "./devices/DeviceProfiles";
import {TagDropdown} from "../components/TagDropdown";
import {TagsState} from "../reducers/tags";
import {
    index as fetchTags, IndexActionRequest,
    post as createTag, PostActionRequest as PostTagActionRequest
} from '../actions/tags';
import {Tag} from "../models";
import {JSONAPIObject, JSONAPIRelationship} from "../json-api";

interface ReduxStateProps {
    device: DeviceState;
    tags: TagsState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        device: state.device,
        tags: state.tags
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
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        push,
        inventory,
        test,
        fetchTags,
        fetchDeviceIfRequired,
        createTag,
        patchRelationship
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

@connect<ReduxStateProps, ReduxDispatchProps, DevicePageProps>(
    mapStateToProps,
    mapDispatchToProps
)
export class DevicePage extends React.Component<DevicePageProps, DevicePageState> {

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

    componentDidMount(): void {
        this.props.fetchDeviceIfRequired(''+this.props.match.params.id, ['tags']);
        this.props.fetchTags();
    }

    render(): JSX.Element {
        const {
            device,
            match: {params: {id: device_id}},
            tags
        } = this.props;

        const tagChoices = tags.items.map((item: JSONAPIObject<Tag>) => {
            return {name: item.attributes.name, text: item.attributes.name, value: item.id};
        });

        let deviceTags: Array<number> = [];
        if (device.device && device.device.relationships) {
            deviceTags = device.device.relationships.tags &&
                device.device.relationships.tags.data.map((t: JSONAPIRelationship) => parseInt(t.id, 0));
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
                                onChange={this.handleApplyTags}
                            />
                            <Segment>
                                {device && <MacOSDeviceDetail device={device}/>}
                            </Segment>
                            <Menu pointing secondary color="purple" inverted>
                                <MenuItemLink to={`/devices/${device_id}/certificates`}>Certificates</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/commands`}>Commands</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/installed_applications`}>Applications</MenuItemLink>
                                <MenuItemLink to={`/devices/${device_id}/installed_profiles`}>Profiles</MenuItemLink>
                            </Menu>
                        </Grid.Column>
                    </Grid.Row>
                    <Grid.Row>
                        <Grid.Column>
                            <Route path='/devices/:id/certificates' component={DeviceCertificates}/>
                            <Route path='/devices/:id/commands' component={DeviceCommands}/>
                            <Route path='/devices/:id/installed_applications' component={DeviceApplications}/>
                            <Route path='/devices/:id/installed_profiles' component={DeviceProfiles}/>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
            </Container>
        );
    }
}