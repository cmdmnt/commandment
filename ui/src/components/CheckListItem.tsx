import * as React from "react";
import List from "semantic-ui-react/src/elements/List";

interface ICheckListItemProps {
    title: string;
    description?: string;
    value: any; // will be interpreted as boolean
    children?: JSX.Element[] | JSX.Element;
}

export const CheckListItem: React.FunctionComponent<ICheckListItemProps> = ({ title, value, description, children }: ICheckListItemProps) => (
    <List.Item>
        {value ? <List.Icon name="checkmark" size="large" /> : <List.Icon name="remove" size="large" />}
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
