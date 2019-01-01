import * as byteSize from "byte-size";
import * as React from "react";
import {CellInfo} from "react-table";

export const ByteSize: React.FunctionComponent<CellInfo> = ({ value, original }) => (
    <span>{value ? byteSize(value)["value"] + " " + byteSize(value)["unit"] : ""}</span>
);
