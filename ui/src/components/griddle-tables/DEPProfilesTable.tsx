import * as React from "react";
import Griddle, {ColumnDefinition, GriddlePageProperties, RowDefinition} from "griddle-react";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SimpleLayout} from "../griddle/SimpleLayout";

export interface IDEPProfilesTableProps {
    data: any;
    pageProperties?: GriddlePageProperties;
}

export const DEPProfilesTable: React.StatelessComponent<IDEPProfilesTableProps> = (props) => (
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
            <ColumnDefinition title="ID" id="id" />
            <ColumnDefinition title="Server Name" id="attributes.profile_name" />
        </RowDefinition>
    </Griddle>
);
