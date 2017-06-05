import * as React from 'react';
import {List} from 'semantic-ui-react';
import {object} from 'prop-types';
import {components} from "griddle-react";

export const ListTableBody = ({ rowIds, Row, style, className }: components.TableBodyProps) => (
    <List divided relaxed style={style} className={className}>
        { rowIds && rowIds.map((r: React.Component<components.RowProps, void>) => <Row key={r} griddleKey={r} />)}
    </List>
);

export const ListTableContainer = (OriginalComponent: React.StatelessComponent<components.TableBodyProps>) => class ListTableComponent extends React.Component<any,any> {

    static contextTypes = {
        components: object
    };

    render() {
        return <this.context.components.TableBody />;
    }
};



