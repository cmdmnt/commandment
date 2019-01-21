import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps} from "react-table";
import {JSONAPIDataObject} from "../../store/json-api";
import {InstalledCertificate} from "../../store/device/types";
import {DEPAccount} from "../../store/dep/types";

export interface IDeviceCertificateTableProps {
    loading: boolean;
    data: Array<JSONAPIDataObject<InstalledCertificate>>;
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Header: "Common Name",
        accessor: (certificate: JSONAPIDataObject<InstalledCertificate>) => certificate.attributes.x509_cn,
        id: "x509_cn",
    },
];

export const DeviceCertificatesTable = ({ data, ...props }: IDeviceCertificateTableProps & Partial<TableProps>) => (
    <ReactTable
        manual
        filterable
        data={data}
        columns={columns}
        {...props}
    />
);
