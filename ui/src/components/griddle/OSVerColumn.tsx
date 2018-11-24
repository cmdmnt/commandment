import * as React from "react";
import {Link} from "react-router-dom";
import {JSONAPIDataObject} from "../../json-api";
import {Device} from "../../models";

interface OSVerColumnProps {
    rowData: JSONAPIDataObject<Device>;
}

export class OSVerColumn extends React.Component<OSVerColumnProps, undefined> {
    public render() {
        const {
            rowData,
        } = this.props;

        let osName = "";

        switch (rowData.attributes.model_name) {
            case "Mac Pro":
            case "iMac":
                osName = "macOS";
                break;
            case "iPhone":
            case "iPad":
                osName = "iOS";
                break;
        }

        return (
            <div>
                <span>{osName} { rowData.attributes.os_version }</span>
            </div>
        )
    }
}
