import * as actions from '../actions/organization';
import {JSONAPIObject, isJSONAPIErrorResponsePayload} from "../json-api";
import {Organization} from "../models";

export interface OrganizationState {
    organization?: Organization;
    loading: boolean;
    error: boolean;
    errorDetail?: any
    lastReceived?: Date;
    submitted: boolean;
}

const initialState: OrganizationState = {
    loading: false,
    error: false,
    submitted: false
};

export type OrganizationAction = actions.ReadActionResponse | actions.PostActionResponse;

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
                organization: action.payload,
                submitted: true
            };
        case actions.READ_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.READ_FAILURE:
            return {
                ...state,
                loading: false,
                error: true,
                errorDetail: action.payload
            };
        case actions.READ_SUCCESS:
            console.dir(action);
            return {
                ...state,
                loading: false,
                organization: action.payload,
                lastReceived: new Date()
            };
        default:
            return state;
    }
}