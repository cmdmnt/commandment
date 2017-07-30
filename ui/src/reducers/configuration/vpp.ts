import * as actions from "../../actions/vpp";
import {VPPAccount} from "../../models";
import {TokenActionResponse} from "../../actions/vpp";
import {isJSONAPIErrorResponsePayload} from "../../json-api";

export interface VPPState {
    data?: VPPAccount;
    loading: boolean;
    submitted: boolean;
    error: boolean;
    errorDetail?: any;
}

const initialState: VPPState = {
    loading: false,
    error: false,
    submitted: false
};

type VPPAction = TokenActionResponse;

export function vpp(state: VPPState = initialState, action: VPPAction): VPPState {
    switch (action.type) {
        case actions.TOKEN_REQUEST:
            return {
                ...state,
                loading: true
            };
        case actions.TOKEN_SUCCESS:
            return {
                ...state,
                loading: false,
                data: action.payload
            };
        case actions.TOKEN_FAILURE:
            return {
                ...state,
                error: true
            };
        default:
            return state;
    }
}