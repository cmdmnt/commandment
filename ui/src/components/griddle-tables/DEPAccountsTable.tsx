import * as React from "react";
import Griddle, {ColumnDefinition, GriddlePageProperties, RowDefinition} from "griddle-react";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SimpleLayout} from "../griddle/SimpleLayout";
import {SinceNowUTC} from "../griddle/SinceNowUTC";

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
            <ColumnDefinition title="Organization" id="attributes.org_name" />
            <ColumnDefinition title="Server Name" id="attributes.server_name" />
            <ColumnDefinition title="Token Expires" id="attributes.access_token_expiry" customComponent={SinceNowUTC} />
        </RowDefinition>
    </Griddle>
);
