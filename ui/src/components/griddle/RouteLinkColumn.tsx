import * as React from 'react';
import {Link} from 'react-router-dom';
import {components} from "griddle-react";


export const RouteLinkColumn = (value: components.ColumnDefinitionProps): JSX.Element => {
    return <Link to={value.cellProperties.urlPrefix + value.value}>{value.value}</Link>;
};