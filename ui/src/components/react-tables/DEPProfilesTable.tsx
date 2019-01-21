import * as React from "react";
import ReactTable, {TableProps, Column} from "react-table";
import selectTableHoc from "react-table/lib/hoc/selectTable";
import {DEPAccount, DEPProfile} from "../../store/dep/types";
import {DEPProfileName} from "../react-table/DEPProfileName";
import {JSONAPIDataObject} from "../../store/json-api";
// import "react-table/react-table.css";

export interface IDEPProfilesTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<DEPProfile>>;
    onToggleSelection: () => void;
    onToggleAll: () => void;
}

const columns: Column[] = [
    {
        Cell: DEPProfileName,
        Header: "Name",
        accessor: "attributes.profile_name",
        id: "profile_name",
    },
    {
        Header: "UUID",
        accessor: "attributes.uuid",
        id: "uuid",
    },
];

const ReactSelectTable = selectTableHoc(ReactTable);

export const DEPProfilesTable = ({ data, ...props }: IDEPProfilesTableProps & Partial<TableProps>) => (
    <ReactSelectTable
        keyField="id"
        selectType="checkbox"
        data={data}
        columns={columns}
        {...props}
    />
);
