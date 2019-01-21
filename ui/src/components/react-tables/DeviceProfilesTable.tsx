import * as React from "react";
import ReactTable, {TableProps} from "react-table";
import {InstalledProfile} from "../../store/device/types";
import {JSONAPIDataObject} from "../../store/json-api";
import {DEPAccount} from "../../store/dep/types";

export interface IDeviceProfilesTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<InstalledProfile>>;
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

export const DeviceProfilesTable = ({ data, ...props }: IDeviceProfilesTableProps & Partial<TableProps>) => (
    <ReactTable
        manual
        filterable
        data={data}
        columns={columns}
        {...props}
    />
);
