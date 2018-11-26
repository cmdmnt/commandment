import * as React from "react";
import {Link} from "react-router-dom";
import {JSONAPIDataObject} from "../../json-api";
import {Device} from "../../store/device/types";
import {ModelIcon} from "../ModelIcon";

interface DeviceColumnProps {
    rowData: JSONAPIDataObject<Device>;
}

export class DeviceColumn extends React.Component<DeviceColumnProps, undefined> {
    public render() {
        const {
            rowData,
        } = this.props;

        return (
            <div>
                <Link to={`/devices/${rowData.id}`}>
                    <span>{ rowData.attributes.device_name ?
                        rowData.attributes.device_name :
                        `DEP ${rowData.attributes.description}`  }</span>
                </Link>
            </div>
        )
    }
}
