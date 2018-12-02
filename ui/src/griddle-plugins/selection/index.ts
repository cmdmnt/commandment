import {SelectionCellContainer} from "./components/SelectionCellContainer";
import {SelectionCellEnhancer} from "./components/SelectionCellEnhancer";
import {TOGGLE_ROW_SELECTION} from "./reducers";
import {selectionSelector, selectedSelector} from "./selectors";

export interface ISelectionPluginState {
    selectionPlugin: {
        selection: string[];
    }
}

const initialState: ISelectionPluginState = {
    selectionPlugin: {
        selection: ["4"],
    },
};

export const SelectionPlugin = (config?: any) => {
    return {
        components: {
            CellContainer: SelectionCellContainer,
            CellEnhancer: SelectionCellEnhancer,
        },
        initialState,
        reducers: {
            TOGGLE_ROW_SELECTION,
        },
        selectors: {
            selectedSelector,
            selectionSelector,
        },
    }
};
