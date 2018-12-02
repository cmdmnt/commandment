import * as React from "react";
import {Link} from "react-router-dom";
import {CellInfo} from "react-table";

export const DeviceName: React.FunctionComponent<CellInfo> = ({ value, original }) => (
    <Link to={`/devices/${original.id}`}>
        <span>{value ? value : original.attributes.description}</span>
    </Link>
);
