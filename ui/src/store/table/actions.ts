import {ActionCreator} from "redux";

export enum TableActionTypes {
    TOGGLE_SELECTION = "@react_table/TOGGLE_SELECTION",
    TOGGLE_ALL = "@react_table/TOGGLE_ALL",
}

export type ToggleSelectionActionCreator = (key: string, shiftKeyPressed: boolean, row: any) => IToggleSelectionAction;
export interface IToggleSelectionAction {
    key: string;
    shiftKeyPressed: boolean;
    row: any;
    type: TableActionTypes;
}

export const toggleSelection: ActionCreator<IToggleSelectionAction> =
    (key: string, shiftKeyPressed: boolean, row: any) => {
    return {
        key,
        row,
        shiftKeyPressed,
        type: TableActionTypes.TOGGLE_SELECTION,
    };
};

export interface IToggleAllAction {
    type: TableActionTypes;
}

export const toggleAll = (): ActionCreator<IToggleAllAction> => {
    return {
        type: TableActionTypes.TOGGLE_ALL,
    };
};

export type TableActions = IToggleSelectionAction & IToggleAllAction;
