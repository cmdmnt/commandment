import * as React from 'react';
import {components} from 'griddle-react';

export const SelectableRow = (props: components.RowProps) => {
    const {Cell, griddleKey, columnIds, style, className} = props;

    const onClick = () => {
        // console.dir(rowData);
        // console.dir(rowProperties);
    };

    return (
        <tr
            key={griddleKey}
            style={style}
            className={className}
            onClick={onClick}
        >
            { columnIds && columnIds.map((c: number) => (
                <Cell
                    key={`${c}-${griddleKey}`}
                    griddleKey={griddleKey}
                    columnId={c}
                    style={style}
                    className={className}
                />
            ))}
        </tr>
    );
};
