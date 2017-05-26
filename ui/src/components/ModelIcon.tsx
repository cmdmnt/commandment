import * as React from 'react';
import {Icon} from 'semantic-ui-react';

interface ModelIconProps {
    value: string;
    title: string;
}

export const ModelIcon = (props: ModelIconProps): JSX.Element => {
    const icons: { [propName: string]: string; } = {
       'iMac': 'desktop',
       'MacBook Pro': 'laptop',
       'MacBook Air': 'laptop',
       'Mac Pro': 'trash',
       'iPhone': 'mobile'
    };

    let className = 'question';
    if (icons.hasOwnProperty(props.value)) {
        className = icons[props.value];
    }

    return <Icon name={className} bordered circular title={props.title || props.value} />;
};