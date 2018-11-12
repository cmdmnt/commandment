import Griddle, {ColumnDefinition, components, GriddlePageProperties, RowDefinition} from "griddle-react";
import {Map} from "immutable";
import * as React from "react";
import {connect} from "react-redux";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {DEPAccountColumn} from "../griddle/DEPAccountColumn";
import {SimpleLayout} from "../griddle/SimpleLayout";
import {SinceNowUTC} from "../griddle/SinceNowUTC";

export interface IDEPAccountsTableProps {
    data: any;
    pageProperties?: GriddlePageProperties;
}

const rowDataSelector = (state: Map<string, any>, { griddleKey }: { griddleKey?: string }) => {
    return state
        .get("data")
        .find((rowMap: any) => rowMap.get("griddleKey") === griddleKey)
        .toJSON();
};

const enhancedWithRowData = connect((state, props: components.RowProps) => {
    return {
        // rowData will be available into MyCustomComponent
        rowData: rowDataSelector(state, props),
    };
});

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
            <ColumnDefinition title="Server Name" id="id,attributes.server_name"
                              customComponent={enhancedWithRowData(DEPAccountColumn)} />
            <ColumnDefinition title="Organization" id="attributes.org_name" />
            <ColumnDefinition title="Token Expires" id="attributes.access_token_expiry" customComponent={SinceNowUTC} />
        </RowDefinition>
    </Griddle>
);
