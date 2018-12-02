import Griddle, {ColumnDefinition, RowDefinition} from "griddle-react";
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui";
import {SelectionPlugin} from "../../griddle-plugins/selection";
import {SimpleLayout} from "../griddle/SimpleLayout";
import {ModelIcon} from "../ModelIcon";
import {DeviceColumn} from "../griddle/DeviceColumn";
import {OSVerColumn} from "../griddle/OSVerColumn";
import {SinceNowUTC} from "../griddle/SinceNowUTC";
import Grid from "semantic-ui-react/src/collections/Grid/Grid";
import * as React from "react";

// export const DevicesTable = () => (
//     <Griddle
//         data={devices.items}
//         pageProperties={{
//             currentPage: griddleState.currentPage,
//             pageSize: griddleState.pageSize,
//             recordCount: devices.recordCount,
//         }}
//         styleConfig={{
//             classNames: {
//                 Table: "ui celled table",
//             },
//         }}
//         events={this.props.events}
//         plugins={[SemanticUIPlugin(), SelectionPlugin()]}
//         components={{
//             Layout: SimpleLayout,
//         }}
//     >
//         <RowDefinition onClick={() => console.log("fmeh")}>
//             <ColumnDefinition title="Type" id="attributes.model_name"
//                               customComponent={ModelIcon} width={60} style={{textAlign: "center"}} />
//             <ColumnDefinition title="Name" id="id,attributes.model_name,attributes.device_name"
//                               customComponent={enhancedWithRowData(DeviceColumn)}/>
//             <ColumnDefinition title="Serial" id="attributes.serial_number"
//                               width={140} />
//             <ColumnDefinition title="OS" id="attributes.model_name,attributes.os_version"
//                               customComponent={enhancedWithRowData(OSVerColumn)}/>
//             <ColumnDefinition title="Last Seen" id="attributes.last_seen"
//                               customComponent={SinceNowUTC}/>
//         </RowDefinition>
//     </Griddle>
// );
