import * as React from "react";
import {CellInfo} from "react-table";
import {Icon} from "semantic-ui-react";
import {FunctionComponent, ReactElement} from "react";

const icons: { [status: string]: ReactElement } = {
    "appstore_mac": <Icon name="laptop" color="grey" />,
    "appstore_ios": <Icon name="mobile" color="grey" />,
};

export const ApplicationType: FunctionComponent<CellInfo> = ({ value }: CellInfo) => (
    <span>{icons.hasOwnProperty(value) ? icons[value] : null}</span>
);
