import * as React from "react";
import Icon from "semantic-ui-react/src/elements/Icon";
import {SemanticICONS} from "semantic-ui-react/src";

interface ModelIconProps {
    value: string;
    title: string;
}

export const ModelIcon = (props: ModelIconProps): JSX.Element => {
    const icons: { [propName: string]: SemanticICONS; } = {
       "iMac": "desktop",
       "iPhone": "mobile alternate",
       "iPad": "tablet alternate",
       "MacBook Air": "laptop",
       "MacBook Pro": "laptop",
       "Mac Pro": "computer",
    };

    let className: SemanticICONS = "apple";
    if (icons.hasOwnProperty(props.value)) {
        className = icons[props.value];
    }

    return <Icon name={className} size="large" title={props.title || props.value} />;
};
