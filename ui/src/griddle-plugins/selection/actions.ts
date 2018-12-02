
export enum SelectionPluginActionTypes {
    TOGGLE_ROW_SELECTION = "TOGGLE_ROW_SELECTION",
}

export interface IToggleRowSelectionAction {
    type: SelectionPluginActionTypes.TOGGLE_ROW_SELECTION;
    id: string;
}

export function toggleSelection(id: string): IToggleRowSelectionAction {
    console.log("toggle selection " + id);
    return {
        id,
        type: SelectionPluginActionTypes.TOGGLE_ROW_SELECTION,
    };
}
