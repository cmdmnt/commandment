import {FunctionComponent} from "react";
import {DeviceState} from "../../store/device/reducer";
import * as React from "react";
import {format} from "date-fns";
import {
    Divider,
    Grid,
    Button,
    Header,
    List,
    Message
} from "semantic-ui-react";

export interface IDEPDeviceDetailProps {
    device: DeviceState;
}

export const DEPDeviceDetail: FunctionComponent<IDEPDeviceDetailProps> =
    ({device, ...props}: IDEPDeviceDetailProps) => {

    return (
        <div className="DEPDeviceDetail">
            <Divider hidden />
            <Header as="h1">
                {device.device.attributes.description}
                <Header.Subheader>SN: {device.device.attributes.serial_number}</Header.Subheader>
            </Header>

            <Message>DEP Device - Not yet enrolled</Message>

            <Grid columns={2}>
                <Grid.Row>
                    <Grid.Column>
                        <List>
                            <List.Item>
                                <List.Icon name="cube" size="large" verticalAlign="middle" />
                                <List.Content>
                                    <List.Header>Model</List.Header>
                                    <List.Description>{device.device.attributes.model}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="paint brush" size="large" verticalAlign="middle" />
                                <List.Content>
                                    <List.Header>Colour</List.Header>
                                    <List.Description>{device.device.attributes.color}</List.Description>
                                </List.Content>
                            </List.Item>
                        </List>
                    </Grid.Column>
                    <Grid.Column>
                        <List>
                            <List.Item>
                                <List.Icon name="calendar" size="large" verticalAlign="middle" />
                                <List.Content>
                                    <List.Header>Assigned to this MDM</List.Header>
                                    <List.Description>{format(device.device.attributes.device_assigned_date)}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="user" size="large" verticalAlign="middle" />
                                <List.Content>
                                    <List.Header>Assigned by Apple ID</List.Header>
                                    <List.Description>{device.device.attributes.device_assigned_by}</List.Description>
                                </List.Content>
                            </List.Item>
                            <List.Item>
                                <List.Icon name="cloud" size="large" verticalAlign="middle" />
                                <List.Content>
                                    <List.Header>Profile Status</List.Header>
                                    <List.Description>{device.device.attributes.profile_status}</List.Description>
                                </List.Content>
                            </List.Item>
                        </List>
                    </Grid.Column>
                </Grid.Row>
            </Grid>

            <Button>Assign DEP Profile</Button>
        </div>
    );
};
