export type ROW_SELECTED = 'selection/ROW_SELECTED';
export const ROW_SELECTED: ROW_SELECTED = 'selection/ROW_SELECTED';

export interface RowSelectedAction {
    type: ROW_SELECTED;
    selected: Array<any>;
}

export function selectRow(): RowSelectedAction {
    return {
        type: ROW_SELECTED,
        selected: []
    }
}

