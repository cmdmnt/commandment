import * as React from "react";
import ReactTable, {TableProps} from "react-table";
import {AvailableOSUpdate, Command} from "../../store/device/types";
import {SinceNowUTC} from "../griddle/SinceNowUTC";

export interface IDeviceCommandsTableProps {
    loading: boolean;
    data: Command[];
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Header: "Type",
        accessor: "attributes.request_type",
        id: "request_type",
    },
    {
        Header: "Status",
        accessor: "attributes.status",
        id: "status",
    },
    {
        Header: "Sent",
        accessor: "attributes.sent_at",
        id: "sent",
    },
];

export const DeviceCommandsTable = ({ data, ...props }: IDeviceCommandsTableProps & TableProps) => (
    <ReactTable
        manual
        filterable
        keyField="id"
        data={data}
        columns={columns}
        {...props}
    />
);
