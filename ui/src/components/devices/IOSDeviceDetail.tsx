import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import {DeviceState} from "../../store/device/reducer";

import {Route} from "react-router";
import {DeviceRename} from "../../containers/DeviceRename";
import {DeviceApplications} from "../../containers/devices/DeviceApplications";
import {DeviceCertificates} from "../../containers/devices/DeviceCertificates";
import {DeviceCommands} from "../../containers/devices/DeviceCommands";
import {DeviceDetail} from "../../containers/devices/DeviceDetail";
import {DeviceOSUpdates} from "../../containers/devices/DeviceOSUpdates";
import {DeviceProfiles} from "../../containers/devices/DeviceProfiles";
import {
    ClearPasscodeActionRequest, InventoryActionRequest, LockActionRequest,
    PushActionRequest,
    RestartActionRequest,
    ShutdownActionRequest,
    TestActionRequest,
} from "../../store/device/actions";
import {ButtonLink} from "../semantic-ui/ButtonLink";
import {MenuItemLink} from "../semantic-ui/MenuItemLink";
import {TagDropdown} from "../TagDropdown";

import Divider from "semantic-ui-react/dist/commonjs/elements/Divider/Divider";
import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import Grid from "semantic-ui-react/src/collections/Grid";
import Menu from "semantic-ui-react/src/collections/Menu";
import Button from "semantic-ui-react/src/elements/Button";
import Header from "semantic-ui-react/src/elements/Header";
import List from "semantic-ui-react/src/elements/List";
import {DropdownItemProps} from "semantic-ui-react/src/modules/Dropdown/DropdownItem";

import {SyntheticEvent} from "react";
import {DropdownProps} from "semantic-ui-react/src/modules/Dropdown";
import {ITagsState} from "../../store/tags/reducer";
import "./MacOSDeviceDetail.scss";

interface IIOSDeviceDetailProps {
    device: DeviceState;
    tags: ITagsState;
    deviceTags: number[];

    onAddTag: (event: SyntheticEvent<any>, data: object) => void;
    onChangeTag: (event: SyntheticEvent<HTMLElement>, data: DropdownProps) => void;
    onSearchTag: (value: string) => void;

    clearPasscode: ClearPasscodeActionRequest;
    inventory: InventoryActionRequest;
    lock: LockActionRequest;
    push: PushActionRequest;
    restart: RestartActionRequest;
    shutdown: ShutdownActionRequest;
}

export const IOSDeviceDetail: React.FunctionComponent<IIOSDeviceDetailProps> = ({
                                                                                    device,
                                                                                    tags, deviceTags,
                                                                                    clearPasscode,
                                                                                    inventory,
                                                                                    lock,
                                                                                    push,
                                                                                    restart,
                                                                                    shutdown,
                                                                                    onAddTag, onChangeTag, onSearchTag,
                                                                                }: IIOSDeviceDetailProps) => {

    if (!device.device) {
        return (<div className="IOSDeviceDetail">No device</div>);
    }

    const attributes = device.device.attributes;

    const niceLastSeen = attributes.last_seen ? distanceInWordsToNow(attributes.last_seen, {addSuffix: true}) : "Never";

    return (
        <div className="IOSDeviceDetail">
            <Divider hidden/>
            <Header as="h1">
                {device.device.attributes.device_name}
                <Header.Subheader>SN: {device.device.attributes.serial_number}</Header.Subheader>
            </Header>

            <TagDropdown
                loading={tags.loading}
                tags={tags.items}
                value={deviceTags}
                onAddItem={onAddTag}
                onSearch={onSearchTag}
                onChange={onChangeTag}
            />
            <Divider hidden/>
            <Grid columns={2} className="MacOSDeviceDetail">
                <Grid.Row>
                    <Grid.Column>
                        <List>
                            <List.Item>
                                <List.Icon name="heartbeat" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>Last Seen</List.Header>
                                    <List.Description>{niceLastSeen}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="disk outline" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>iOS</List.Header>
                                    <List.Description>{attributes.os_version} ({attributes.build_version})</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="tag" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>UDID</List.Header>
                                    <List.Description>{attributes.udid}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="desktop" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>Model</List.Header>
                                    <List.Description>{attributes.model}</List.Description>
                                </List.Content>
                            </List.Item>
                        </List>

                    </Grid.Column>
                    <Grid.Column>
                        <List>
                            <List.Item>
                                <List.Icon name="bluetooth alternative" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>Bluetooth MAC</List.Header>
                                    <List.Description>{attributes.bluetooth_mac || "Not Available"}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="wifi" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>Wifi MAC</List.Header>
                                    <List.Description>{attributes.wifi_mac || "Not Available"}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="eye" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>Supervised</List.Header>
                                    <List.Description>{attributes.is_supervised ? "Yes" : "No"}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="mobile" size="large" verticalAlign="middle"/>
                                <List.Content>
                                    <List.Header>IMEI</List.Header>
                                    <List.Description>{attributes.imei}</List.Description>
                                </List.Content>
                            </List.Item>
                        </List>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Divider/>
                        <Button icon labelPosition="left"
                                disabled={!device.device.attributes.is_supervised}
                                onClick={() => restart(device.device.id)}>
                            <Icon name="refresh"/>
                            Restart
                        </Button>
                        <Button icon labelPosition="left"
                                disabled={!device.device.attributes.is_supervised}
                                onClick={() => shutdown(device.device.id)}>
                            <Icon name="arrow down"/>
                            Shut down
                        </Button>
                        <Button icon labelPosition="left" onClick={() => clearPasscode(device.device.id)}>
                            <Icon name="delete"/>
                            Clear Passcode
                        </Button>
                        <Button icon labelPosition="left" onClick={() => lock(device.device.id)}>
                            <Icon name="lock"/>
                            Lock
                        </Button>
                        <Button icon labelPosition="left" onClick={() => inventory(device.device.id)}>
                            <Icon name="search"/>
                            Full Inventory
                        </Button>
                        <Button icon labelPosition="left" onClick={() => push(device.device.id)}>
                            <Icon name="pushed"/>
                            Blank Push
                        </Button>
                        <ButtonLink to={`/devices/${device.device.id}/rename`}>
                            Rename
                        </ButtonLink>
                        <Menu pointing secondary color="purple" inverted>
                            <MenuItemLink to={`/devices/${device.device.id}/detail`}>Detail</MenuItemLink>
                            <MenuItemLink to={`/devices/${device.device.id}/certificates`}>Certificates</MenuItemLink>
                            <MenuItemLink to={`/devices/${device.device.id}/commands`}>Commands</MenuItemLink>
                            <MenuItemLink
                                to={`/devices/${device.device.id}/installed_applications`}>Applications</MenuItemLink>
                            <MenuItemLink to={`/devices/${device.device.id}/installed_profiles`}>Profiles</MenuItemLink>
                            <MenuItemLink
                                to={`/devices/${device.device.id}/available_os_updates`}>Updates</MenuItemLink>
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
        </div>
    );
};
