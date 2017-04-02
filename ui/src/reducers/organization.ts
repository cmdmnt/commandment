import * as actions from '../actions/organization';

export interface OrganizationState {
    organization?: any;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
}

const initialState: OrganizationState = {
    loading: false,
    error: false
};

export function config(state: OrganizationState = initialState, action: actions.PostActionResponse): OrganizationState {
    switch (action.type) {
        case POST_REQUEST:
            return {
                ...state,
                loading: true
            };
        case POST_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case POST_SUCCESS:
            return {
                ...state,
                loading: false,
                config: action.payload.data
            };
        default:
            return state;
    }
}