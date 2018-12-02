import {components} from "griddle-react";
import * as React from "react";

export interface ISelectionColumnDefinition extends components.ColumnDefinitionProps {
    onChange: (e: Event) => void;
}

export class SelectionColumnDefinition extends React.Component<ISelectionColumnDefinition, any> {
    public render(): JSX.Element {
        return null;
    }
}
