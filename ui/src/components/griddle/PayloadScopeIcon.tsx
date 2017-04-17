import * as React from 'react';

interface GriddleValue {
    griddleKey: number;
    value: any;
}

export const PayloadScopeIcon = (value: GriddleValue): JSX.Element => {
    const icons: { [propName: string]: string; } = {
       'System': 'fa-computer',
       'User': 'fa-user'
    };

    return <i className={'fa ' + icons[value.value]} />;
};