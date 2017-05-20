import * as React from 'react';
import * as moment from 'moment';
import * as Griddle from 'griddle-react';

interface CommandStatusProps {

}

export const CommandStatus: React.StatelessComponent<CommandStatusProps> = (value: any) => {
    console.dir(arguments);
    return <span>{value}</span>;
};