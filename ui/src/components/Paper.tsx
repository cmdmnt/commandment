// Loosely modelled after material-ui's paper element
import * as React from 'react';

import './Paper.scss';

export const Paper = (props: any) => {
    return (
        <div className='Paper'>{props.children}</div>
    )
};