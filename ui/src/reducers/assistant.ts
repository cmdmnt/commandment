import * as actions from '../actions/assistant';

export interface AssistantState {
    totalSteps: number;
    currentStep: number;
}

const initialState: AssistantState = {
    totalSteps: 0,
    currentStep: 0
};

export function assistant(state: AssistantState = initialState, action: any): AssistantState {
    switch (action.type) {
        default:
            return state
    }
}