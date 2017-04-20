import * as React from 'react';
import {Link} from 'react-router-dom';

interface GriddleValue {
    griddleKey: number;
    value: any;
}

export const DeviceLink = (value: GriddleValue): JSX.Element => {
    return <Link to={`/devices/${value.value}`}>{value.value}</Link>;
};