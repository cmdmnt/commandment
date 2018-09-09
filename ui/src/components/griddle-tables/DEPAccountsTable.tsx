import * as React from "react";
import Griddle, {ColumnDefinition, GriddlePageProperties, RowDefinition} from "griddle-react";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SimpleLayout} from "../griddle/SimpleLayout";

export interface IDEPAccountsTableProps {
    data: any;
    pageProperties?: GriddlePageProperties;
}

export const DEPAccountsTable: React.StatelessComponent<IDEPAccountsTableProps> = (props) => (
    <Griddle
        data={props.data}
        pageProperties={props.pageProperties}
        styleConfig={{
            classNames: {
                Table: "ui celled table",
            },
        }}
        plugins={[SemanticUIPlugin(), SelectionPlugin()]}
        components={{ Layout: SimpleLayout }}
    >
        <RowDefinition>
            <ColumnDefinition title="ID" id="attributes.id" />
            <ColumnDefinition title="Server Name" id="attributes.server_name" />
        </RowDefinition>
    </Griddle>
);
