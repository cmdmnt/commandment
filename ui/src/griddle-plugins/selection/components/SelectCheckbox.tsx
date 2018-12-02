import {components} from "griddle-react";
import * as React from "react";

export const SelectCheckbox = (props: components.ColumnDefinitionProps) => (
    <input type="checkbox" value={props.value} onChange={(e) => { e.preventDefault(); props.toggleSelection(props.value) }} checked={props.selected} />
);
