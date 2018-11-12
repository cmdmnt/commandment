import Griddle, {ColumnDefinition, GriddlePageProperties, RowDefinition} from "griddle-react";
import * as React from "react";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {SimpleLayout} from "../griddle/SimpleLayout";
import {RouteLinkColumn} from "../griddle/RouteLinkColumn";

export interface IDEPProfilesTableProps {
    data: any;
    depAccountId: string;
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
            <ColumnDefinition title="ID" id="id" customComponent={RouteLinkColumn}
                              urlPrefix={`/dep/accounts/${props.depAccountId}/profiles/`} />
            <ColumnDefinition title="Name" id="attributes.profile_name" />
        </RowDefinition>
    </Griddle>
);
