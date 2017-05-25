import {SelectableRow} from "./components/SelectableRow";
import SelectableRowDefinition from "./components/SelectableRowDefinition";

export const SelectionPlugin = (config: any) => {
    return {
        components: {
            Row: SelectableRow,
            RowDefinition: SelectableRowDefinition
        }
    }
};
