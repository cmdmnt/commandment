import * as React from "react";
import ReactTable, {Column, TableProps} from "react-table";
import selectTableHoc from "react-table/lib/hoc/selectTable";

import {Application} from "../../store/applications/types";
import {JSONAPIDataObject} from "../../store/json-api";
import {AppName} from "../react-table/AppName";
import {ApplicationType} from "../react-table/ApplicationType";
// import "react-table/react-table.css";

export interface IApplicationsTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<Application>>;
    onToggleSelection: () => void;
    onToggleAll: () => void;
}

const columns: Column[] = [
    {
        Cell: ApplicationType,
        Header: "Type",
        accessor: "attributes.discriminator",
        id: "discriminator",
        style: { textAlign: "center" },
        width: 50,
    },
    {
        Cell: AppName,
        Header: "Name",
        accessor: "attributes.display_name",
        id: "display_name",
    },
    {
        Header: "Version",
        accessor: "attributes.version",
        id: "version",
    },
];

const ReactSelectTable = selectTableHoc(ReactTable);

export const ApplicationsTable = ({ data, ...props }: IApplicationsTableProps & TableProps) => (
    <ReactSelectTable
        keyField="id"
        selectType="checkbox"
        data={data}
        columns={columns}
        {...props}
    />
);
