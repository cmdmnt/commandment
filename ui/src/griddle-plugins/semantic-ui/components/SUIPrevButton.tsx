import * as React from 'react';
import {Menu, Icon} from 'semantic-ui-react';

interface SUIPrevButtonProps {
    className: string;
    style: { [propName: string]: any };
    hasPrevious: boolean;
    onClick: () => void;
}

export const SUIPrevButton = ({ className, style, hasPrevious, onClick }: SUIPrevButtonProps) => (
    <Menu.Item as='a' icon className={className} style={style} onClick={onClick} disabled={!hasPrevious}>
        <Icon name='left chevron'/>
    </Menu.Item>
);