import {distanceInWordsToNow} from "date-fns";
import * as React from "react";
import ReactTable, {CellInfo, TableProps} from "react-table";
import {JSONAPIDataObject} from "../../json-api";
import {InstalledCertificate} from "../../store/device/types";

export interface IDeviceCertificateTableProps {
    loading: boolean;
    data: InstalledCertificate[];
    onFetchData: (state: any, instance: any) => void;
}

const columns = [
    {
        Header: "Common Name",
        accessor: (certificate: JSONAPIDataObject<InstalledCertificate>) => certificate.attributes.x509_cn,
        id: "x509_cn",
    },
];

export const DeviceCertificatesTable = ({ data, ...props }: IDeviceCertificateTableProps & TableProps) => (
    <ReactTable
        manual
        filterable
        keyField="id"
        data={data}
        columns={columns}
        {...props}
    />
);
