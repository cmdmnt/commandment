import * as React from 'react';

interface IOSDeviceDetailState {

}

interface IOSDeviceDetailProps {
    device: Device;
}


export class IOSDeviceDetail extends React.Component<IOSDeviceDetailProps, IOSDeviceDetailState> {

    render() {

        let os_version = '10.2';

        return (
            <div className='IOSDeviceDetail'>
                battery level

                power button / shutdown / restart

                passcode present and we have permission - clearpasscode button

            </div>
        )
    }

}