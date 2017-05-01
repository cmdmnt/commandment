import {RowEnhancer} from './components/RowEnhancer';
import {SelectableRow} from "./components/SelectableRow";

export const SelectionPlugin = (config: any) => {
    return {
        components: {
            Row: SelectableRow
        }
    }
};
