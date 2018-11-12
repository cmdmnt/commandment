import {components} from "griddle-react";
import * as React from "react";
import {Link} from "react-router-dom";

export const RouteLinkColumn = (value: components.ColumnDefinitionProps): JSX.Element => {
    return <Link to={value.cellProperties.urlPrefix + value.value}>{value.value}</Link>;
};
