import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {SimpleLayout as Layout} from "../griddle/SimpleLayout";
import {RouteLinkColumn} from "../griddle/RouteLinkColumn";
import {PayloadScopeIcon} from "../griddle/PayloadScopeIcon";
import Grid from "semantic-ui-react/src/collections/Grid/Grid";
import * as React from "react";
//
// export const ProfilesTable = () => (
//     <Griddle
//         data={profiles.items}
//         plugins={[SemanticUIPlugin()]}
//         pageProperties={{
//             currentPage: griddleState.currentPage,
//             pageSize: griddleState.pageSize,
//             recordCount: profiles.recordCount,
//         }}
//         styleConfig={{
//             classNames: {
//                 Table: "ui celled table",
//                 NoResults: "ui message",
//             },
//         }}
//         events={this.props.events}
//         components={{
//             Layout,
//         }}
//     >
//         <RowDefinition>
//             <ColumnDefinition id="id" customComponent={RouteLinkColumn} urlPrefix="/profiles/" />
//             <ColumnDefinition title="Name" id="attributes.display_name" />
//             <ColumnDefinition title="Scope" id="attributes.scope" component={PayloadScopeIcon} />
//             <ColumnDefinition title="UUID" id="attributes.uuid" />
//         </RowDefinition>
//     </Griddle>
// )


// componentWillMount?(): void {
//     this.props.index(this.props.griddleState.pageSize, this.props.griddleState.currentPage);
// }
//
// componentWillUpdate?(nextProps: ProfilesPageProps, nextState: void | Readonly<{}>) {
//     const {griddleState} = this.props;
// const {griddleState: nextGriddleState} = nextProps;
//
// if (nextGriddleState.filter !== griddleState.filter
//     || nextGriddleState.currentPage !== griddleState.currentPage
//     || nextGriddleState.sortId !== griddleState.sortId
//     || nextGriddleState.sortAscending !== griddleState.sortAscending
// ) {
//     let sortColumnId = "";
//     if (nextGriddleState.sortId) {
//         sortColumnId = nextGriddleState.sortId.substr("attributes.".length);
//         if (!nextGriddleState.sortAscending) {
//             sortColumnId = "-" + sortColumnId;
//         }
//     }
//
//     this.props.index(
//         nextGriddleState.pageSize,
//         nextGriddleState.currentPage,
//         [sortColumnId],
//         [{ name: "display_name", op: "ilike", val: `%${nextGriddleState.filter}%` }]);
// }
// }