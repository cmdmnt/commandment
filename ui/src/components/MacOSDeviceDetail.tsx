import * as React from 'react';
import {DeviceState} from "../reducers/device";

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

        return (
            <div className='MacOSDeviceDetail'>
                <div className='row'>
                    <div className='column'>
                        <dl>
                            <dt>UDID</dt>
                            <dd>{attributes.udid}</dd>

                            <dt>Device Name</dt>
                            <dd>{attributes.device_name}</dd>

                            <dt>Serial Number</dt>
                            <dd>{attributes.serial_number}</dd>

                            <dt>Model</dt>
                            <dd>{attributes.model}</dd>

                            <dt>Model Name</dt>
                            <dd>{attributes.model_name}</dd>

                            <dt>OS Version</dt>
                            <dd>{attributes.os_version}</dd>

                            <dt>Product Name</dt>
                            <dd>{attributes.product_name}</dd>
                        </dl>
                    </div>
                </div>
            </div>
        )
    }

}