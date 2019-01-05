import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps} from "react-table";
import selectTableHoc from "react-table/lib/hoc/selectTable";
import {JSONAPIDataObject} from "../../store/json-api";
// import "react-table/react-table.css";
import {Device} from "../../store/device/types";
import {ModelIcon} from "../devices/ModelIcon";
import {DeviceName} from "../react-table/DeviceName";
import {DEPAccount} from "../../store/dep/types";

export interface IDevicesTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<Device>>;
    toggleSelection: (key: string, shiftKeyPressed: boolean, row: any) => any;
    toggleAll: () => any;
    isSelected: (key: string) => boolean;
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Cell: ModelIcon,
        Header: "",
        accessor: "attributes.model_name",
        filterable: false,
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
        Cell: (props: CellInfo) => props.value ? distanceInWordsToNow(props.value, {addSuffix: true}) : "never",
        Header: "Last Seen",
        accessor: "attributes.last_seen",
        filterable: false,
        id: "last_seen",
    },
];

const ReactSelectTable = selectTableHoc(ReactTable);

export const DevicesTable = ({ data, ...props }: IDevicesTableProps & TableProps) => (
    <ReactSelectTable
        manual
        filterable
        keyField="id"
        selectType="checkbox"
        data={data}
        columns={columns}
        {...props}
    />
);
