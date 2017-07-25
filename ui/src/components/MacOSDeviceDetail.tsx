import * as React from 'react';
import * as moment from 'moment';
import {DeviceState} from "../reducers/device";
import {ModelIcon} from "./ModelIcon";
import { Button, Header, Icon, Grid, List } from 'semantic-ui-react';
import './MacOSDeviceDetail.scss';

interface MacOSDeviceDetailState {

}

interface MacOSDeviceDetailProps {
    device: DeviceState;
}


export class MacOSDeviceDetail extends React.Component<MacOSDeviceDetailProps, MacOSDeviceDetailState> {

    render(): JSX.Element {
        const {
            device
        } = this.props;
        
        if (!device.device) {
            return (<div className='MacOSDeviceDetail'>No device</div>)
        }

        const attributes = device.device.attributes;

        const name = attributes.device_name ? attributes.device_name : '(Untitled)';
        const niceLastSeen = attributes.last_seen ? moment(attributes.last_seen).fromNow() : 'Never';

        return (
            <Grid columns={3} className='MacOSDeviceDetail'>
                <Grid.Row>
                    <Grid.Column>
                        <Header as="h1">{name} <Button content='Rename' /></Header>
                        <p>{attributes.hostname}</p>
                    </Grid.Column>
                    <Grid.Column>
                        <Header as="h1" color="grey" textAlign='right'>{attributes.serial_number}</Header>
                    </Grid.Column>
                </Grid.Row>
                <Grid.Row>
                    <Grid.Column>
                        <List>
                            <List.Item>
                                <List.Icon name='heartbeat' size='large' verticalAlign='middle' />
                                <List.Content>
                                    <List.Header>Last Seen</List.Header>
                                    <List.Description>{niceLastSeen}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name='disk outline' size='large' verticalAlign='middle' />
                                <List.Content>
                                    <List.Header>macOS</List.Header>
                                    <List.Description>{attributes.os_version} ({attributes.build_version})</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name='tag' size='large' verticalAlign='middle' />
                                <List.Content>
                                    <List.Header>UDID</List.Header>
                                    <List.Description>{attributes.udid}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name='desktop' size='large' verticalAlign='middle' />
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
                                <List.Icon name='bluetooth alternative' size='large' verticalAlign='middle' />
                                <List.Content>
                                    <List.Header>Bluetooth MAC</List.Header>
                                    <List.Description>{attributes.bluetooth_mac || 'Not Available'}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name='wifi' size='large' verticalAlign='middle' />
                                <List.Content>
                                    <List.Header>Wifi MAC</List.Header>
                                    <List.Description>{attributes.wifi_mac || 'Not Available'}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name='protect' size='large' verticalAlign='middle' />
                                <List.Content>
                                    <List.Header>SIP</List.Header>
                                    <List.Description>{attributes.sip_enabled ? 'Enabled' : 'Disabled'}</List.Description>
                                </List.Content>
                            </List.Item>
                        </List>
                    </Grid.Column>
                    <Grid.Column>

                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }

}