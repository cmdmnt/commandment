import * as React from 'react';
import * as moment from 'moment';
import {DeviceState} from "../reducers/device";
import {ModelIcon} from "./griddle/ModelIcon";
import { Button, Header } from 'semantic-ui-react';

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
            <div className='MacOSDeviceDetail'>
                <Header floated="right" as="h1" color="grey"><small>{attributes.serial_number}</small></Header>
                <Header as="h1"><ModelIcon value={attributes.model_name} /> {name}</Header>

                <div className='row'>
                    <div className='column'>
                        <dl className='horizontal'>
                            <dt>Last Seen</dt>
                            <dd>{niceLastSeen}</dd>

                            <dt>macOS</dt>
                            <dd>{attributes.os_version} ({attributes.build_version})</dd>
                            
                            <dt>UDID</dt>
                            <dd>{attributes.udid}</dd>

                            <dt>Model</dt>
                            <dd>{attributes.model}</dd>
                        </dl>
                    </div>
                </div>
            </div>
        )
    }

}