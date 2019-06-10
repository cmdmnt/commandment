import * as React from "react";
import {SemanticICONS} from "semantic-ui-react";
import {Icon} from "semantic-ui-react";

interface IModelIconProps {
    value: string;
    title: string;
}

export const ModelIcon = (props: IModelIconProps): JSX.Element => {
    const icons: { [propName: string]: SemanticICONS; } = {
       "Mac Pro": "computer",
       "MacBook Air": "laptop",
       "MacBook Pro": "laptop",
       "iMac": "desktop",
       "iPad": "tablet",
       "iPhone": "mobile",
    };

    let className: SemanticICONS = "apple";
    if (icons.hasOwnProperty(props.value)) {
        className = icons[props.value];
    }

    return <Icon name={className} size="large" title={props.title || props.value} />;
};
