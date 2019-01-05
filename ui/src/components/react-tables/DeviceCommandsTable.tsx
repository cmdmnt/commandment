import * as React from "react";
import ReactTable, {TableProps} from "react-table";
import {Command} from "../../store/device/types";
import {RelativeToNow} from "../react-table/RelativeToNow";
import {CommandStatus} from "../react-table/CommandStatus";
import {JSONAPIDataObject} from "../../store/json-api";
import {DEPAccount} from "../../store/dep/types";

export interface IDeviceCommandsTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<Command>>;
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Cell: CommandStatus,
        Header: "Status",
        accessor: "attributes.status",
        id: "status",
        maxWidth: 50,
        style: { textAlign: "center" },
    },
    {
        Header: "Type",
        accessor: "attributes.request_type",
        id: "request_type",
    },
    {
        Cell: RelativeToNow,
        Header: "Sent",
        accessor: "attributes.sent_at",
        id: "sent_at",
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
