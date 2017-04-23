import * as React from 'react';

interface GriddleValue {
    griddleKey?: number;
    value: any;
}

export const ModelIcon = (value: GriddleValue): JSX.Element => {
    const icons: { [propName: string]: string; } = {
       'iMac': 'fa-desktop',
       'MacBook Pro': 'fa-laptop',
       'MacBook Air': 'fa-laptop',
       'MacPro': 'fa-trash',
       'iPhone': 'fa-mobile'
    };

    let className = 'fa fa-question-circle';
    if (icons.hasOwnProperty(value.value)) {
        className = 'fa ' + icons[value.value];
    }

    return <i className={className} title={value.value} />;
};