import * as React from 'react';
import { components } from 'griddle-react';

export const SelectableRow = ({Cell, griddleKey, columnIds, style, className}: components.RowProps) => (
    <tr
        key={griddleKey}
        style={style}
        className={className}
        onClick={() => console.log('asd')}
    >
        { columnIds && columnIds.map(c => (
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
