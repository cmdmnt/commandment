import * as React from 'react';
import {ModelIcon} from "../ModelIcon";
import {Link} from 'react-router-dom';


interface DeviceColumnProps {

}

export class DeviceColumn extends React.Component<DeviceColumnProps, undefined> {
    render () {
        const {
            rowData
        } = this.props;

        console.log('props follow');
        console.dir(this.props);

        return (
            <div>
                <Link to={`/devices/${rowData.id}`}>
                <ModelIcon value={rowData.attributes.model_name} title={rowData.attributes.product_name} />
                <span>{ rowData.attributes.device_name }</span>
                </Link>
            </div>
        )
    }
}