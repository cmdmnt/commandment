import * as actions from "./actions";

export interface IAssistantState {
    currentStep: number;
    totalSteps: number;
}

const initialState: IAssistantState = {
    currentStep: 0,
    totalSteps: 0,
};

export type AssistantAction = actions.NextStepAction | actions.PrevStepAction;

export function assistant(state: IAssistantState = initialState, action: AssistantAction): IAssistantState {
    switch (action.type) {
        case actions.NEXT_STEP:
            return {
                ...state,
                currentStep: (state.currentStep + 1),
            };
        case actions.PREV_STEP:
            return {
                ...state,
                currentStep: (state.currentStep - 1),
            };
        default:
            return state
    }
}
