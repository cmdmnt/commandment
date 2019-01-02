import * as React from "react";
import ReactTable, {TableProps} from "react-table";
import {InstalledProfile} from "../../store/device/types";

export interface IDeviceProfilesTableProps {
    loading: boolean;
    data: InstalledProfile[];
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Header: "Display Name",
        accessor: "attributes.payload_display_name",
        id: "payload_display_name",
    },
    {
        Header: "Identifier",
        accessor: "attributes.payload_identifier",
        id: "payload_identifier",
    },
];

export const DeviceProfilesTable = ({ data, ...props }: IDeviceProfilesTableProps & TableProps) => (
    <ReactTable
        manual
        filterable
        keyField="id"
        data={data}
        columns={columns}
        {...props}
    />
);
