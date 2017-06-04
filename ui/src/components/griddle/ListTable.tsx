/// <reference path="../../typings/griddle.d.ts" />
import * as React from 'react';
import {List} from 'semantic-ui-react';
import {object} from 'prop-types';
import {RowProps, TableBodyProps} from "griddle-react";

export const ListTableBody = ({ rowIds, Row, style, className }: TableBodyProps) => (
    <List divided relaxed style={style} className={className}>
        { rowIds && rowIds.map((r: React.Component<RowProps, void>) => <Row key={r} griddleKey={r} />)}
    </List>
);

export const ListTableContainer = (OriginalComponent: React.StatelessComponent<TableBodyProps>) => class ListTableComponent extends React.Component<any,any> {

    static contextTypes = {
        components: object
    };

    render() {
        return <this.context.components.TableBody />;
    }
};



