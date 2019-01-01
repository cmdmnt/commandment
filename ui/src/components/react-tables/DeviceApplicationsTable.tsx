import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps} from "react-table";
import {JSONAPIDataObject} from "../../json-api";
import {InstalledCertificate} from "../../store/device/types";
import {ByteSize} from "../react-table/ByteSize";

export interface IDeviceApplicationsTableProps {
    loading: boolean;
    data: InstalledCertificate[];
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Header: "Name",
        accessor: "attributes.name",
        id: "name",
    },
    {
        Header: "Version",
        accessor: "attributes.short_version",
        id: "short_version",
        maxWidth: 140,
    },
    {
        Cell: ByteSize,
        Header: "Size",
        accessor: "attributes.bundle_size",
        id: "bundle_size",
        maxWidth: 100,
    },
];

export const DeviceApplicationsTable = ({ data, ...props }: IDeviceApplicationsTableProps & TableProps) => (
    <ReactTable
        manual
        filterable
        keyField="id"
        data={data}
        columns={columns}
        {...props}
    />
);
