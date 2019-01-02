import * as React from "react";
import ReactTable, {TableProps} from "react-table";
import {AvailableOSUpdate} from "../../store/device/types";

export interface IDeviceUpdatesTableProps {
    loading: boolean;
    data: AvailableOSUpdate[];
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Header: "Product ID",
        accessor: "attributes.product_key",
        id: "product_key",
        maxWidth: 140,
    },
    {
        Header: "Name",
        accessor: "attributes.human_readable_name",
        id: "human_readable_name",
    },
    {
        Header: "Version",
        accessor: "attributes.version",
        id: "version",
        maxWidth: 100,
    },
];

export const DeviceUpdatesTable = ({ data, ...props }: IDeviceUpdatesTableProps & TableProps) => (
    <ReactTable
        manual
        filterable
        keyField="id"
        data={data}
        columns={columns}
        {...props}
    />
);
