import * as React from "react";
import {Icon, Menu, SemanticICONS} from "semantic-ui-react";

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
