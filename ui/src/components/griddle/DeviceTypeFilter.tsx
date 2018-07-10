import * as React from 'react';
import Button from 'semantic-ui-react/src/elements/Button/Button';

export type DeviceTypeFilterValues = 'all' | 'iphone' | 'ipad' | 'mac' | 'appletv';

export interface IDeviceTypeFilterProps {
    selected: DeviceTypeFilterValues;
    onClick: (selected: DeviceTypeFilterValues) => void;
}

export const DeviceTypeFilter: React.StatelessComponent<IDeviceTypeFilterProps> = (
    props = {selected: 'all', onClick: (v) => {}},
    context) => (
    <Button.Group>
        <Button icon='asterisk' title='All Device Types' active={props.selected == 'all'} onClick={() => {props.onClick('all')}} />
        <Button icon='mobile alternate' title='iPhone' active={props.selected == 'iphone'} onClick={() => {props.onClick('iphone')}} />
        <Button icon='tablet alternate' title='iPad' active={props.selected == 'ipad'} onClick={() => {props.onClick('ipad')}} />
        <Button icon='computer' title='Mac' active={props.selected == 'mac'} onClick={() => {props.onClick('mac')}} />
        <Button icon='tv' title='AppleTV' active={props.selected == 'appletv'} onClick={() => {props.onClick('appletv')}} />
    </Button.Group>
);
