import {ReadActionResponse, PostActionResponse} from '../../actions/configuration/scep';
import * as actions from "../../actions/configuration/scep";
import {SCEPConfiguration} from "../../models";

export interface SCEPState {
    data?: SCEPConfiguration;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: SCEPState = {
    loading: false,
    error: false,
    submitted: false
};

type SCEPAction = ReadActionResponse | PostActionResponse;

export function scep(state: SCEPState = initialState, action: SCEPAction): SCEPState {
    switch (action.type) {
        case actions.READ_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload
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
                error: true
            };
        case actions.POST_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.POST_FAILURE:
            return {
                ...state,
                error: true,
                loading: false
            };
        case actions.POST_SUCCESS:
            return {
                ...state,
                error: false,
                loading: false,
                submitted: true
            };

        default:
            return state;
    }
}