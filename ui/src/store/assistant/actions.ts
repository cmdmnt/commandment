import {ThunkAction} from 'redux-thunk';

export type NEXT_STEP = 'assistant/NEXT_STEP';
export const NEXT_STEP: NEXT_STEP = 'assistant/NEXT_STEP';

export type PREV_STEP = 'assistant/PREV_STEP';
export const PREV_STEP: PREV_STEP = 'assistant/PREV_STEP';

export interface NextStepAction {
    type: NEXT_STEP;
}

export interface PrevStepAction {
    type: PREV_STEP;
}

export const nextStep = (): NextStepAction => {
    return {
        type: NEXT_STEP
    };
};

export const prevStep = (): PrevStepAction => {
    return {
        type: PREV_STEP
    };
};

