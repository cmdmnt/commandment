import * as actions from '../actions/assistant';

export interface AssistantState {
    totalSteps: number;
    currentStep: number;
}

const initialState: AssistantState = {
    totalSteps: 0,
    currentStep: 0
};

export type AssistantAction = actions.NextStepAction | actions.PrevStepAction;

export function assistant(state: AssistantState = initialState, action: AssistantAction): AssistantState {
    switch (action.type) {
        case actions.NEXT_STEP:
            return {
                ...state,
                currentStep: (state.currentStep + 1)
            };
        case actions.PREV_STEP:
            return {
                ...state,
                currentStep: (state.currentStep - 1)
            };
        default:
            return state
    }
}