import * as React from 'react';

interface GriddleValue {
    griddleKey: number;
    value: any;
}

export const ModelIcon = (value: GriddleValue): JSX.Element => {
    console.log(value);
    const icons: { [propName: string]: string; } = {
       'iMac': 'fa-computer',
       'iPhone': 'fa-mobile'
    };

    return <i className={'fa ' + icons[value.value]} />;
};