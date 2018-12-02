import {components, selectors} from "griddle-react";
import { Map } from "immutable";

export const selectionSelector = (state: Map<string, any>): string[] =>
    state.getIn(["selectionPlugin", "selection"], []);

// Determine whether the current row is selected.
export const selectedSelector = (state: Map<string, any>, props: components.CellProps): boolean => {
    const value: string | number = selectors.cellValueSelector(state, props);
    const selection = selectionSelector(state);
    return selection.indexOf("" + value) !== -1;
};
