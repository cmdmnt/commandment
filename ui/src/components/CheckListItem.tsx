import * as React from 'react';
import { List } from 'semantic-ui-react';

interface CheckListItemProps {
    title: string;
    description?: string;
    value: any; // will be interpreted as boolean
    children?: JSX.Element[];
}

export const CheckListItem: React.StatelessComponent<CheckListItemProps> = ({ title, value, description, children }: CheckListItemProps) => (
    <List.Item>
        {value ? <List.Icon name='checkmark' size='large' /> : <List.Icon name='remove' size='large' />}
        <List.Content>
            <List.Header>{title}</List.Header>
            {children &&
                <List>
                    {children}
                </List>
            }
        </List.Content>
    </List.Item>
);