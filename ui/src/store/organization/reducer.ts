import * as actions from "./actions";
import {isJSONAPIErrorResponsePayload, JSONAPIDataObject} from "../../json-api";
import {Organization} from "./types";

export interface OrganizationState {
    organization?: Organization;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    submitted: boolean;
}

const initialState: OrganizationState = {
    error: false,
    loading: false,
    submitted: false,
};

export type OrganizationAction = actions.ReadActionResponse | actions.PostActionResponse;

export function organization(state: OrganizationState = initialState, action: OrganizationAction): OrganizationState {
    switch (action.type) {
        case actions.POST_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case actions.POST_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
                loading: false,
            };
        case actions.POST_SUCCESS:
            return {
                ...state,
                loading: false,
                organization: action.payload,
                submitted: true,
            };
        case actions.READ_REQUEST:
            return {
                ...state,
                loading: true,
            };
        case actions.READ_FAILURE:
            return {
                ...state,
                error: true,
                errorDetail: action.payload,
                loading: false,
            };
        case actions.READ_SUCCESS:
            return {
                ...state,
                lastReceived: new Date(),
                loading: false,
                organization: action.payload,
            };
        default:
            return state;
    }
}
