import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps, Column} from "react-table";
import selectTableHoc from "react-table/lib/hoc/selectTable";
import {JSONAPIDataObject} from "../../store/json-api";
// import "react-table/react-table.css";
import {AvailableOSUpdate, Device} from "../../store/device/types";
import {Profile} from "../../store/profiles/types";
import {DeviceName} from "../react-table/DeviceName";
import {ProfileName} from "../react-table/ProfileName";

export interface IProfilesTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<Profile>>;
    onToggleSelection: () => void;
    onToggleAll: () => void;
}

const columns: Column[] = [
    {
        Cell: ProfileName,
        Header: "Name",
        accessor: (device: JSONAPIDataObject<Device>) => device.attributes.device_name,
        id: "display_name",
    },
    {
        Header: "UUID",
        accessor: "attributes.uuid",
        id: "uuid",
    },
];

const ReactSelectTable = selectTableHoc(ReactTable);

export const ProfilesTable = ({ data, ...props }: IProfilesTableProps & TableProps) => (
    <ReactSelectTable
        manual
        keyField="id"
        selectType="checkbox"
        data={data}
        columns={columns}
        {...props}
    />
);
