import * as React from "react";
import {Link} from "react-router-dom";
import {CellInfo} from "react-table";

export const DEPAccountServerName: React.FunctionComponent<CellInfo> = ({ value, original }) => (
    <Link to={`/dep/accounts/${original.id}`}>
        <span>{value ? value : original.attributes.server_name}</span>
    </Link>
);
