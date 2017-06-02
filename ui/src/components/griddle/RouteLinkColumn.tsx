import * as React from 'react';
import {Link} from 'react-router-dom';
import {ColumnDefinitionProps} from "griddle-react";


export const RouteLinkColumn = (value: ColumnDefinitionProps): JSX.Element => {
    return <Link to={value.cellProperties.urlPrefix + value.value}>{value.value}</Link>;
};