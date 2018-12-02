import {createSelector} from "reselect";
import * as selectors from "./selectors";

export const MultiAttrCellPlugin = (config: any) => {
    return {
        selectors: {
            cellValueSelector: selectors.cellValueSelector,
        },
    }
};
