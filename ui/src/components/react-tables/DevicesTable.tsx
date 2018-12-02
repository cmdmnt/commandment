import * as React from "react";
import ReactTable from "react-table";
import {JSONAPIDataObject} from "../../json-api";
// import "react-table/react-table.css";
import {Device} from "../../store/device/types";
import {ModelIcon} from "../ModelIcon";
import {DeviceName} from "../react-table/DeviceName";

export interface IDevicesTableProps {
    loading: boolean;
    data: Device[];
}

const columns = [
    {
        Cell: ModelIcon,
        Header: "",
        accessor: "attributes.model_name",
        id: "model_name",
        maxWidth: 40,
        style: { textAlign: "center" },
    },
    {
        Cell: DeviceName,
        Header: "Name",
        accessor: (device: JSONAPIDataObject<Device>) => device.attributes.device_name,
        id: "device_name",
    },
    {
        Header: "Serial",
        accessor: "attributes.serial_number",
        id: "serial_number",
    },
    {
        Header: "OS",
        accessor: "attributes.os_version",
        id: "os_version",
        maxWidth: 100,
    },
    {
        Header: "Last Seen",
        accessor: "attributes.last_seen",
        id: "last_seen",
    },
];

export const DevicesTable = (props: IDevicesTableProps) => (
    <ReactTable
        manual
        data={props.data}
        columns={columns} />
);
