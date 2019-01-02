import * as React from "react";
import {Link} from "react-router-dom";
import {CellInfo} from "react-table";

export const DEPProfileName: React.FunctionComponent<CellInfo> = ({ value, original }) => (
    <Link to={`/dep/accounts/${original.attributes.dep_account_id}/profiles/${original.id}`}>
        <span>{value ? value : original.attributes.profile_name}</span>
    </Link>
);
