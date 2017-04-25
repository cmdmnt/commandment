import {ReadActionResponse, PostActionResponse} from '../../actions/configuration/scep';
import * as actions from "../../actions/configuration/scep";

export interface SCEPState {
    data?: SCEPConfiguration;
    loading: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: SCEPState = {
    loading: false,
    error: false
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

        default:
            return state;
    }
}