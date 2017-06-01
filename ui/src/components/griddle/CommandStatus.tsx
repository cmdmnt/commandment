import * as React from 'react';

interface CommandStatusProps {

}

export const CommandStatus: React.StatelessComponent<CommandStatusProps> = (value: any) => {
    return <span>{value}</span>;
};