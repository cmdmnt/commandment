import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps} from "react-table";
import {JSONAPIDataObject} from "../../store/json-api";
import {ManagedApplication} from "../../store/applications/types";

export interface IAppDeployStatusTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<ManagedApplication>>;
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {

    },
    {
        Header: "Bundle ID",
        accessor: "attributes.bundle_id",
        id: "bundle_id",
    },
    {
        Header: "Status",
        accessor: "attributes.status",
        id: "status",
    },
];

export const AppDeployStatusTable = ({ data, ...props }: IAppDeployStatusTableProps & Partial<TableProps>) => (
    <ReactTable
        manual
        filterable
        data={data}
        columns={columns}
        {...props}
    />
);
