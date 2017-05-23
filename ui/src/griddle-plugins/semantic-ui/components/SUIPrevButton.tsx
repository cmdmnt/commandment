import * as React from 'react';
import {Menu, Icon} from 'semantic-ui-react';

interface SUIPrevButtonProps {
    className: string;
    style: { [propName: string]: any };
    hasNext: boolean;
    onClick: () => void;
}

export const SUIPrevButton = ({ className, style, hasNext, onClick }: SUIPrevButtonProps) => (
    <Menu.Item as='a' icon className={className} style={style} onClick={onClick}>
        <Icon name='left chevron'/>
    </Menu.Item>
);