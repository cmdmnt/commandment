
export type NEXT_STEP = 'assistant/NEXT_STEP';
export const NEXT_STEP: NEXT_STEP = 'assistant/NEXT_STEP';

export type PREV_STEP = 'assistant/PREV_STEP';
export const PREV_STEP: PREV_STEP = 'assistant/PREV_STEP';

export type SET_LENGTH = 'assistant/SET_LENGTH';
export const SET_LENGTH: SET_LENGTH = 'assistant/SET_LENGTH';

export interface NextStepAction {
    type: NEXT_STEP;
}

export interface PrevStepAction {
    type: PREV_STEP;
}

export interface SetLengthAction {
    type: SET_LENGTH;
}
