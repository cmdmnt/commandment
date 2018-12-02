import {components} from "griddle-react";
import * as React from "react";

export interface ISelectCellProps extends components.CellProps {
    onSelect: (e: Event) => void;
}

export const SelectCell = ({
   value,
   onClick,
   onMouseEnter,
   onMouseLeave,
   style,
   className,
   onSelect }: ISelectCellProps) => (
    <td
        onClick={onClick}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
        style={style}
        className={className}
    >
        <input type="checkbox" value={value} onChange={onSelect} />
    </td>
);
