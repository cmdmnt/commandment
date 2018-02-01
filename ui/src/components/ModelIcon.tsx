import * as React from "react";
import {Icon, SemanticICONS} from "semantic-ui-react";

interface ModelIconProps {
    value: string;
    title: string;
}

export const ModelIcon = (props: ModelIconProps): JSX.Element => {
    const icons: { [propName: string]: SemanticICONS; } = {
       "iMac": "desktop",
       "iPhone": "mobile",
       "MacBook Air": "laptop",
       "MacBook Pro": "laptop",
       "Mac Pro": "trash",
    };

    let className: SemanticICONS = "question";
    if (icons.hasOwnProperty(props.value)) {
        className = icons[props.value];
    }

    return <Icon name={className} bordered circular title={props.title || props.value} />;
};
