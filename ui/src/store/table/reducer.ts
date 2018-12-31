import {Reducer} from "redux";
import {TableActions, TableActionTypes} from "./actions";

export interface ITableState {
    pageSize: number;
    pages: number;
    selection: string[];
}

const initialState: ITableState = {
    pageSize: 20,
    pages: 0,
    selection: [],
};

export const table: Reducer<ITableState, TableActions> = (state = initialState, action) => {
    switch (action.type) {
        case TableActionTypes.TOGGLE_ALL:
            return state;
        case TableActionTypes.TOGGLE_SELECTION:
            let selection = [...state.selection];
            const keyIndex = state.selection.indexOf(action.key);
            if (keyIndex !== -1) {
                selection = [
                    ...selection.slice(0, keyIndex),
                    ...selection.slice(keyIndex + 1),
                ];
            } else {
                selection.push(action.key);
            }

            return {
                ...state,
                selection,
            };
        default:
            return state;
    }
};
