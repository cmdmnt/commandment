import * as React from 'react';
import * as moment from 'moment';

interface GriddleValue {
    griddleKey: number;
    value: any;
}

export const SinceNowUTC = (value: GriddleValue): JSX.Element => {
    return <span>{moment(value.value).fromNow()}</span>;
};