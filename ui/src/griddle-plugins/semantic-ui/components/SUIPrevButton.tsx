import * as React from "react";
import Icon from "semantic-ui-react/src/elements/Icon";
import {SemanticICONS} from "semantic-ui-react/src";
import Menu from "semantic-ui-react/src/collections/Menu";

interface SUIPrevButtonProps {
    className: string;
    style: { [propName: string]: any };
    hasPrevious: boolean;
    onClick: () => void;
}

export const SUIPrevButton = ({ className, style, hasPrevious, onClick }: SUIPrevButtonProps) => (
    <Menu.Item as="a" icon className={className} style={style} onClick={onClick} disabled={!hasPrevious}>
        <Icon name={"left chevron" as SemanticICONS} />
    </Menu.Item>
);
