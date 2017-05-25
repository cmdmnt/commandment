import * as React from 'react';

export const SelectableRow = (props) => {
    const {Cell, griddleKey, columnIds, style, className, rowData, rowProperties} = props;

    console.dir(props);

    const onClick = () => {
        console.dir(rowData);
        console.dir(rowProperties);
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
