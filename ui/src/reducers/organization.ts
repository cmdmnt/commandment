import * as actions from '../actions/organization';

export interface OrganizationState {
    organization?: Organization;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: OrganizationState = {
    loading: false,
    error: false
};

export type OrganizationAction = actions.IndexActionResponse | actions.PostActionResponse;

export function organization(state: OrganizationState = initialState, action: OrganizationAction): OrganizationState {
    switch (action.type) {
        case actions.POST_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.POST_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case actions.POST_SUCCESS:
            return {
                ...state,
                loading: false,
                config: action.payload.data
            };
        default:
            return state;
    }
}