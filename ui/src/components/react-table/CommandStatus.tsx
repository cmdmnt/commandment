import * as React from "react";
import {CellInfo} from "react-table";
import {Icon, IconProps} from "semantic-ui-react";
import {FunctionComponent, ReactElement} from "react";

const icons: { [status: string]: JSX.Element } = {
    "CommandStatus.Acknowledged": <Icon name="check" color="grey" />,
    "CommandStatus.Error": <Icon name="ban" color="red" />,
    "CommandStatus.NotNow": <Icon name="question circle outline" color="blue" />,
    "CommandStatus.Queued": <Icon name="wait" color="blue" />,
    "CommandStatus.Sent": <Icon name="paper plane" color="green" />,
};

export const CommandStatus: FunctionComponent<CellInfo> = ({ value }: CellInfo) => (
    <span>{icons.hasOwnProperty(value) ? icons[value] : null}</span>
);
