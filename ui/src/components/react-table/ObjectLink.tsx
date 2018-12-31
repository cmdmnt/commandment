import * as React from "react";
import {CellInfo} from "react-table";
import {Link} from "react-router-dom";

export const ObjectLink: React.FunctionComponent<CellInfo> = ({ value, original }: CellInfo) => (
    <Link to={`/objtype/id/${original.id}`}>
        <span>{value ? value : original.attributes.display_name}</span>
    </Link>
);
