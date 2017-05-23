import * as React from 'react';
import {Icon} from 'semantic-ui-react';

interface GriddleValue {
    griddleKey?: number;
    value: any;
    selectors: any;
}

export const ModelIcon = (value: GriddleValue): JSX.Element => {
    const icons: { [propName: string]: string; } = {
       'iMac': 'desktop',
       'MacBook Pro': 'laptop',
       'MacBook Air': 'laptop',
       'Mac Pro': 'fa-trash',
       'iPhone': 'mobile'
    };

    let className = 'question';
    if (icons.hasOwnProperty(value.value)) {
        className = icons[value.value];
    }

    return <Icon name={className} bordered circular title={value.value} />;
};