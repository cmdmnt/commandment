import * as React from "react";
import {connect, Dispatch} from "react-redux";
import {RouteComponentProps} from "react-router";
import {bindActionCreators} from "redux";
import {DeviceState} from "../../reducers/device";
import {RootState} from "../../reducers/index";

import Grid from "semantic-ui-react/src/collections/Grid";
import Header from "semantic-ui-react/src/elements/Header";
import List from "semantic-ui-react/src/elements/List";

import {CheckListItem} from "../../components/CheckListItem";

interface ReduxStateProps {
    device: DeviceState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        device: state.device,
    };
}

interface ReduxDispatchProps {

}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({

    }, dispatch);
}

interface DeviceCommandsRouteProps {

}

interface DeviceDetailProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceCommandsRouteProps> {

}

interface DeviceDetailComponentState {

}

class UnconnectedDeviceDetail extends React.Component<DeviceDetailProps, DeviceDetailComponentState> {
    render() {
        const {
            device: {device},
        } = this.props;

        return (
            <Grid columns={2} className="DeviceDetail">
                <Grid.Row>
                    <Grid.Column>
                        <Header>Security</Header>
                        {device &&
                        <List>
                            <CheckListItem title="Firewall Enabled" value={device.attributes.firewall_enabled}>
                                <CheckListItem title="Stealth Mode" value={device.attributes.stealth_mode_enabled}/>
                                <CheckListItem title="Block all incoming" value={device.attributes.block_all_incoming}/>
                            </CheckListItem>
                            <CheckListItem title="Has Passcode" value={device.attributes.passcode_present}>
                                <CheckListItem title="Passcode is compliant" value={device.attributes.passcode_compliant}/>
                                <CheckListItem title="Passcode is compliant with profiles" value={device.attributes.passcode_compliant_with_profiles}/>
                            </CheckListItem>
                            <CheckListItem title="Full Disk Encryption Enabled" value={device.attributes.fde_enabled}>
                                <CheckListItem title="With Personal Recovery Key" value={device.attributes.fde_has_prk}/>
                                <CheckListItem title="With Institutional Recovery Key" value={device.attributes.fde_has_irk}/>
                            </CheckListItem>
                        </List>}
                    </Grid.Column>
                    <Grid.Column>
                        <Header>iTunes and iCloud</Header>
                        {device &&
                        <List>
                            <CheckListItem title="Store account active" value={device.attributes.itunes_store_account_is_active}/>
                        </List>
                        }
                    </Grid.Column>

                </Grid.Row>
            </Grid>
        );
    }
}

export const DeviceDetail = connect<ReduxStateProps, ReduxDispatchProps, any>(
    mapStateToProps,
    mapDispatchToProps,
)(UnconnectedDeviceDetail);
