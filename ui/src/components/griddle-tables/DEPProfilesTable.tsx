import Griddle, {ColumnDefinition, components, GriddlePageProperties, RowDefinition} from "griddle-react";
import {Map} from "immutable";
import * as React from "react";
import {connect} from "react-redux";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {DEPProfileColumn} from "../griddle/DEPProfileColumn";
import {RouteLinkColumn} from "../griddle/RouteLinkColumn";
import {SimpleLayout} from "../griddle/SimpleLayout";

export interface IDEPProfilesTableProps {
    data: any;
    depAccountId: string;
    pageProperties?: GriddlePageProperties;
}

const rowDataSelector = (state: Map<string, any>, { griddleKey }: { griddleKey?: string }) => {
    return state
        .get("data")
        .find((rowMap: any) => rowMap.get("griddleKey") === griddleKey)
        .toJSON();
};

const enhancedWithRowData = connect((state: Map<string, any>, props: components.RowProps) => {
    return {
        // rowData will be available into MyCustomComponent
        rowData: rowDataSelector(state, props),
    };
});

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
            <ColumnDefinition title="Name" id="id" customComponent={enhancedWithRowData(DEPProfileColumn)} />
        </RowDefinition>
    </Griddle>
);
