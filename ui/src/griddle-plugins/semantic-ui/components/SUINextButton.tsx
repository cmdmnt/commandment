import * as React from "react";
import Icon from "semantic-ui-react/src/elements/Icon";
import {SemanticICONS} from "semantic-ui-react/src";
import Menu from "semantic-ui-react/src/collections/Menu";

interface SUINextButtonProps {
    className: string;
    style: { [propName: string]: any };
    hasNext: boolean;
    onClick: () => void;
}

export const SUINextButton = ({ className, style, hasNext, onClick }: SUINextButtonProps) => (
    <Menu.Item as="a" icon className={className} style={style} onClick={onClick} disabled={!hasNext} >
        <Icon name={"right chevron" as SemanticICONS}/>
    </Menu.Item>
);
