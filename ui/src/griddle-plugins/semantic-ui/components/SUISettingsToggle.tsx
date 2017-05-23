import * as React from 'react';
import {Button} from 'semantic-ui-react';

interface SUISettingsToggleProps {
    onClick: () => void;
    text: string;
    style: any;
    className: string;
}

export const SUISettingsToggle: React.StatelessComponent<SUISettingsToggleProps> = ({ onClick, text, style, className }) => (
    <Button onClick={onClick} style={style} className={className}>{text}</Button>
);


