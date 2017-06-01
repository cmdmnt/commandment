/// <reference path="../../typings/griddle.d.ts" />
import * as React from 'react';
import {RowProps, TableBodyProps} from 'griddle-react';
import {List} from 'semantic-ui-react';
import {object} from 'prop-types';

export const ListTableContainer = OriginalComponent => class ListTableComponent extends React.Component {

    static contextTypes = {
        components: object
    };

    render() {
        return <this.context.components.TableBody />;
    }
};



export const ListTableBody = ({ rowIds, Row, style, className }: TableBodyProps) => (
    <List divided relaxed style={style} className={className}>
        { rowIds && rowIds.map((r: React.Component<RowProps, void>) => <Row key={r} griddleKey={r} />)}
    </List>
);