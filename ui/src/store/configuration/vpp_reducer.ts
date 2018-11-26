import {IVPPAction, TokenActionResponse, VPPActionTypes} from "./vpp";
import {VPPAccount} from "./types";

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
        case VPPActionTypes.TOKEN_REQUEST:
            return {
                ...state,
                loading: true
            };
        case VPPActionTypes.TOKEN_SUCCESS:
            return {
                ...state,
                data: action.payload,
                loading: false,
            };
        case VPPActionTypes.TOKEN_FAILURE:
            return {
                ...state,
                error: true
            };
        default:
            return state;
    }
}
