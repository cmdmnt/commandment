import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps, Column} from "react-table";
import selectTableHoc from "react-table/lib/hoc/selectTable";
import {JSONAPIDataObject} from "../../store/json-api";
import {DEPAccount} from "../../store/dep/types";
import {DEPAccountServerName} from "../react-table/DEPAccountServerName";
// import "react-table/react-table.css";

export interface IDEPAccountsTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<DEPAccount>>;
    onToggleSelection: () => void;
    onToggleAll: () => void;
}

const columns: Column[] = [
    {
        Cell: DEPAccountServerName,
        Header: "Server Name",
        accessor: "attributes.server_name",
        id: "server_name",
    },
    {
        Header: "Organization",
        accessor: "attributes.org_name",
        id: "org_name",
    },
];

const ReactSelectTable = selectTableHoc(ReactTable);

export const DEPAccountsTable = ({ data, ...props }: IDEPAccountsTableProps & TableProps) => (
    <ReactSelectTable
        manual
        keyField="id"
        selectType="checkbox"
        data={data}
        columns={columns}
        {...props}
    />
);
