// import * as actions from "../../actions/vpp";
import {DEPAccount, Device} from "../../models";
// import {TokenActionResponse} from "../../actions/vpp";
import {isJSONAPIErrorResponsePayload, JSONAPIObject} from "../../json-api";

export interface DEPState {
    data?: Array<JSONAPIObject<DEPAccount>>;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: DEPState = {
    loading: false,
    error: false,
    submitted: false
};

// type VPPAction = TokenActionResponse;

export function dep(state: DEPState = initialState, action: any): DEPState {
    switch (action.type) {
        // case actions.TOKEN_REQUEST:
        //     return {
        //         ...state,
        //         loading: true
        //     };
        // case actions.TOKEN_SUCCESS:
        //     return {
        //         ...state,
        //         loading: false,
        //         data: action.payload
        //     };
        // case actions.TOKEN_FAILURE:
        //     return {
        //         ...state,
        //         error: true
        //     };
        default:
            return state;
    }
}